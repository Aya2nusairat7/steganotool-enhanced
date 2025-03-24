import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from PIL import Image

# Add the parent directory to sys.path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    generate_strong_password, encrypt_message, decrypt_message,
    hide_data_in_image, extract_data_from_image
)

class TestPasswordFunctions(unittest.TestCase):
    def test_generate_password(self):
        """Test password generation function returns a proper string."""
        password = generate_strong_password()
        self.assertIsInstance(password, str)
        self.assertTrue(len(password) >= 8)
        
    def test_encrypt_decrypt(self):
        """Test encryption and decryption works correctly."""
        message = "test message"
        password = "testpassword"
        
        encrypted = encrypt_message(message, password)
        self.assertIsInstance(encrypted, bytes)
        
        decrypted = decrypt_message(encrypted, password)
        self.assertEqual(decrypted, message)

class TestImageSteganography(unittest.TestCase):
    @patch('utils.os.path.exists')
    def test_image_functions(self, mock_exists):
        """Test image steganography functions with mocks."""
        mock_exists.return_value = True
        
        # Create a mock image
        with patch('utils.Image.open') as mock_open, \
             patch('utils.np.array') as mock_array, \
             patch('utils.Image.fromarray') as mock_fromarray:
            
            # Setup mocks
            mock_img = MagicMock()
            mock_img.mode = 'RGB'
            mock_img.size = (100, 100)
            mock_open.return_value = mock_img
            
            mock_array.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
            
            mock_new_img = MagicMock()
            mock_fromarray.return_value = mock_new_img
            
            # Test hide_data_in_image
            with patch('utils.Image.open') as mock_open, \
                 patch('builtins.open', unittest.mock.mock_open()), \
                 patch('utils.np.array') as mock_array:
                
                mock_img = MagicMock()
                mock_img.mode = 'RGB'
                mock_img.size = (100, 100)
                mock_open.return_value = mock_img
                
                mock_array.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
                
                # Just test that the function doesn't raise exceptions
                test_data = b"test data"
                try:
                    hide_data_in_image("test.png", "output.png", test_data)
                    # If we get here, the function didn't raise an exception
                    self.assertTrue(True)
                except Exception as e:
                    self.fail(f"hide_data_in_image raised exception {e}")


if __name__ == '__main__':
    unittest.main() 