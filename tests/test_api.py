import unittest
from unittest.mock import patch, MagicMock, mock_open
import io
import os
import sys
import hashlib

# Add the parent directory to sys.path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask app
import api
from flask import Flask

class TestAPIEndpoints(unittest.TestCase):
    """Test the API endpoints."""

    def setUp(self):
        """Set up the test client."""
        self.app = api.app.test_client()
        self.app.testing = True

    def test_index_endpoint(self):
        """Test the index endpoint returns 200 status code."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_health_endpoint(self):
        """Test the health endpoint returns 200 status code."""
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'healthy')

    def test_capabilities_endpoint(self):
        """Test the capabilities endpoint returns 200 status code."""
        response = self.app.get('/api/capabilities')
        self.assertEqual(response.status_code, 200)
        # Check if capabilities exist in response (don't verify values as they depend on utils implementation)
        self.assertIn('image_steganography', response.json)
        self.assertIn('audio_steganography', response.json)

    @patch('utils.convert_and_hide_in_image')
    @patch('utils.generate_strong_password')
    @patch('api.encrypt_message')
    @patch('os.path.getsize')
    def test_encrypt_api_endpoint(self, mock_getsize, mock_encrypt, mock_gen_password, mock_hide_data):
        """Test the encrypt API endpoint."""
        # Setup mocks
        mock_encrypt.return_value = b'encrypted-data'
        mock_gen_password.return_value = 'strong-password'
        mock_hide_data.return_value = None  # No return value needed
        mock_getsize.return_value = 1024  # Fake file size

        # Create test file
        test_data = b'test image data'
        test_file = (io.BytesIO(test_data), 'test.png')

        # Test with auto-generate password
        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=test_data)):
            response = self.app.post(
                '/api/encrypt',
                data={
                    'file': test_file,
                    'message': 'secret message',
                    'auto_generate': 'true',
                    'media_type': 'image'
                },
                content_type='multipart/form-data'
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'success')
            mock_encrypt.assert_called_once()
            mock_gen_password.assert_called_once()
            mock_hide_data.assert_called_once()

    @patch('utils.extract_data_from_image')
    @patch('hashlib.sha256')
    def test_decrypt_api_endpoint(self, mock_sha256, mock_extract_data):
        """Test the decrypt API endpoint."""
        # Create a mock hash object
        mock_hash = MagicMock()
        mock_hash.digest.return_value = b'0123456789abcdef'  # 16-byte mock key
        mock_sha256.return_value = mock_hash

        # Setup extracted data mock (with embedded password)
        # We'll create data that actually works with the XOR decryption algorithm
        password = "testpassword"
        message = "Test message"
        
        # Create encrypted data that will decrypt to our test message
        # with the given password using the XOR algorithm
        key = b'0123456789abcdef'  # Our mock key
        message_bytes = message.encode('utf-8')
        
        # Create "encrypted" data that will decrypt to our message
        encrypted = []
        for i, char in enumerate(message_bytes):
            key_char = key[i % len(key)]
            encrypted_char = char ^ key_char
            encrypted.append(encrypted_char)
            
        encrypted_data = bytes(encrypted)
        
        # Add the marker and password
        extracted_data = encrypted_data + b'\x01' + password.encode('utf-8')
        mock_extract_data.return_value = extracted_data

        # Create test file
        test_data = b'test image data'
        test_file = (io.BytesIO(test_data), 'test.png')

        # Test with embedded password
        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=test_data)):
            response = self.app.post(
                '/api/decrypt',
                data={
                    'file': test_file,
                    'media_type': 'image'
                },
                content_type='multipart/form-data'
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'success')
            mock_extract_data.assert_called_once()

    def test_download_endpoint(self):
        """Test the download endpoint."""
        # This test requires a file to exist in the output folder
        # For this test, we'll mock the send_from_directory function

        with patch('api.send_from_directory') as mock_send:
            mock_send.return_value = "mocked file content"
            response = self.app.get('/api/download/test_file.png')
            self.assertEqual(response.status_code, 200)
            mock_send.assert_called_once()

if __name__ == '__main__':
    unittest.main() 