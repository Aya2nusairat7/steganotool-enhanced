import os
import sys
import requests
import argparse
from pathlib import Path

# Default API URL
API_BASE_URL = "http://localhost:8080/api"

def encrypt_message(api_url, file_path, message, password, media_type="image"):
    """Encrypt a message and hide it in a file using the API"""
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist")
        return False
    
    # Prepare the request
    url = f"{api_url}/encrypt"
    
    # Get file details
    file_name = os.path.basename(file_path)
    
    # Create form data
    files = {
        'file': (file_name, open(file_path, 'rb'), 'application/octet-stream')
    }
    
    form_data = {
        'message': message,
        'password': password,
        'media_type': media_type
    }
    
    print(f"Encrypting message into {file_name} ({media_type})...")
    
    try:
        # Send the request
        response = requests.post(url, files=files, data=form_data)
        
        # Check response
        if response.status_code == 200:
            data = response.json()
            
            # Download the processed file
            download_url = f"{api_url}/download/{data['output_filename']}"
            download_file(download_url, data['output_filename'])
            
            print(f"Success! Encrypted message ({data['message_length']} chars) into {data['output_filename']}")
            print(f"Original file: {data['original_filename']}")
            print(f"Output file size: {data['file_size'] / 1024:.2f} KB")
            print(f"Encrypted data size: {data['encrypted_size']} bytes")
            print(f"Compression ratio: {(1 - data['encrypted_size'] / len(message.encode('utf-8'))) * 100:.1f}%")
            print(f"Output file saved to the current directory")
            return True
        else:
            error = response.json().get('error', 'Unknown error')
            print(f"API Error: {error}")
            return False
    
    except Exception as e:
        print(f"Error during encryption: {str(e)}")
        return False

def decrypt_message(api_url, file_path, password, media_type="image"):
    """Decrypt a message hidden in a file using the API"""
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist")
        return False
    
    # Prepare the request
    url = f"{api_url}/decrypt"
    
    # Get file details
    file_name = os.path.basename(file_path)
    
    # Create form data
    files = {
        'file': (file_name, open(file_path, 'rb'), 'application/octet-stream')
    }
    
    form_data = {
        'password': password,
        'media_type': media_type
    }
    
    print(f"Extracting message from {file_name} ({media_type})...")
    
    try:
        # Send the request
        response = requests.post(url, files=files, data=form_data)
        
        # Check response
        if response.status_code == 200:
            data = response.json()
            
            print(f"Success! Extracted message ({data['message_length']} chars) from {data['filename']}")
            print("\nDecrypted Message:")
            print("-" * 40)
            print(data['message'])
            print("-" * 40)
            return True
        else:
            error = response.json().get('error', 'Unknown error')
            print(f"API Error: {error}")
            return False
    
    except Exception as e:
        print(f"Error during decryption: {str(e)}")
        return False

def download_file(url, filename):
    """Download a file from the API"""
    try:
        response = requests.get(url, stream=True)
        
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        else:
            print(f"Error downloading file: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"Error downloading file: {str(e)}")
        return False

def check_api_health(api_url):
    """Check if the API is online"""
    try:
        response = requests.get(f"{api_url}/health")
        if response.status_code == 200:
            return True
        return False
    except:
        return False

def get_capabilities(api_url):
    """Get the capabilities of the API"""
    try:
        response = requests.get(f"{api_url}/capabilities")
        if response.status_code == 200:
            return response.json()
        return {}
    except:
        return {}

def detect_media_type(file_path):
    """Detect the media type based on file extension"""
    extension = Path(file_path).suffix.lower()
    if extension in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']:
        return 'image'
    elif extension in ['.wav', '.mp3', '.ogg', '.flac', '.aac', '.m4a']:
        return 'audio'
    else:
        return 'image'  # Default to image

def main():
    parser = argparse.ArgumentParser(description="Steganography Client for API")
    parser.add_argument("--url", default=API_BASE_URL, help="Base URL of the API")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Encrypt command
    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt and hide a message")
    encrypt_parser.add_argument("file", help="Path to the file to hide data in")
    encrypt_parser.add_argument("message", help="Message to encrypt and hide")
    encrypt_parser.add_argument("password", help="Password for encryption")
    encrypt_parser.add_argument("--type", choices=["image", "audio"], help="Media type (detected automatically if not specified)")
    
    # Decrypt command
    decrypt_parser = subparsers.add_parser("decrypt", help="Extract and decrypt a hidden message")
    decrypt_parser.add_argument("file", help="Path to the file with hidden data")
    decrypt_parser.add_argument("password", help="Password for decryption")
    decrypt_parser.add_argument("--type", choices=["image", "audio"], help="Media type (detected automatically if not specified)")
    
    # Health check command
    subparsers.add_parser("health", help="Check if the API is online")
    
    # Capabilities command
    subparsers.add_parser("capabilities", help="Get the capabilities of the API")
    
    args = parser.parse_args()
    
    # No command specified
    if not args.command:
        parser.print_help()
        return
    
    # Check API health
    if args.command == "health":
        if check_api_health(args.url):
            print("API is online and healthy")
        else:
            print("API is not responding")
        return
    
    # Get capabilities
    if args.command == "capabilities":
        capabilities = get_capabilities(args.url)
        if capabilities:
            print("API Capabilities:")
            for name, available in capabilities.items():
                status = "Available" if available else "Not Available"
                print(f"- {name}: {status}")
        else:
            print("Could not retrieve API capabilities")
        return
    
    # Encrypt command
    if args.command == "encrypt":
        media_type = args.type if args.type else detect_media_type(args.file)
        encrypt_message(args.url, args.file, args.message, args.password, media_type)
        return
    
    # Decrypt command
    if args.command == "decrypt":
        media_type = args.type if args.type else detect_media_type(args.file)
        decrypt_message(args.url, args.file, args.password, media_type)
        return

if __name__ == "__main__":
    main() 