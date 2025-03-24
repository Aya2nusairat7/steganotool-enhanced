# Steganography Tool User Guide

Welcome to the Steganography Tool User Guide. This document provides practical instructions on how to use the tool for hiding and extracting encrypted messages in media files.

## Getting Started

### Installation

1. Ensure you have Python 3.7 or higher installed on your system
2. Install FFmpeg (required for audio processing)
3. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```
4. Start the server:
   ```
   python api.py
   ```
5. Open a web browser and navigate to http://localhost:8080

### Quick Start

Here are the basic steps to use the tool:

#### To Hide a Message:
1. Select an image or audio file
2. Enter your message
3. Either enter a password or let the system generate one
4. Process the file
5. Download the output file containing your hidden message

#### To Extract a Message:
1. Upload a file containing a hidden message
2. Enter the password (if it's not stored in the file)
3. Extract and view the hidden message

## Using the Web Interface

The web interface provides the most user-friendly way to access all features of the tool.

### Hiding a Message in an Image

1. Open the web interface at http://localhost:8080
2. In the "Encrypt & Hide" section:
   - Select "Image" as the media type
   - Click "Select File" and choose an image file (PNG recommended)
   - Enter your secret message in the "Message to Hide" field
   - Choose one of the password options:
     - Check "Auto-generate secure password" to let the system create a strong password
     - Or enter your own password in the password field
   - Click "Encrypt & Hide"
3. Once processing is complete:
   - You'll see a success message
   - If you used an auto-generated password, it will be displayed (save it somewhere secure)
   - Click "Download File" to save the resulting image with your hidden message

### Hiding a Message in an Audio File

1. Open the web interface at http://localhost:8080
2. In the "Encrypt & Hide" section:
   - Select "Audio" as the media type
   - Click "Select File" and choose an audio file (WAV, MP3, etc.)
   - Enter your secret message in the "Message to Hide" field
   - Choose one of the password options:
     - Check "Auto-generate secure password" to let the system create a strong password
     - Or enter your own password in the password field
   - Click "Encrypt & Hide"
3. Once processing is complete:
   - You'll see a success message
   - If you used an auto-generated password, it will be displayed (save it somewhere secure)
   - Click "Download File" to save the resulting audio file (WAV format) with your hidden message

### Extracting a Message from an Image

1. Open the web interface at http://localhost:8080
2. In the "Extract & Decrypt" section:
   - Select "Image" as the media type
   - Click "Select File" and choose an image containing a hidden message
   - If the password isn't stored in the file, enter it in the password field
   - Click "Extract & Decrypt"
3. Once processing is complete:
   - You'll see the decrypted message displayed
   - If a password was found in the file, it will be shown

### Extracting a Message from an Audio File

1. Open the web interface at http://localhost:8080
2. In the "Extract & Decrypt" section:
   - Select "Audio" as the media type
   - Click "Select File" and choose an audio file containing a hidden message
   - If the password isn't stored in the file, enter it in the password field
   - Click "Extract & Decrypt"
3. Once processing is complete:
   - You'll see the decrypted message displayed
   - If a password was found in the file, it will be shown

## Using the Command-Line Tool

The command-line tool allows for quick operations and can be used in scripts or batch processing.

### Checking API Health

```bash
python client.py health
```

### Viewing API Capabilities

```bash
python client.py capabilities
```

### Hiding a Message in an Image

```bash
python client.py encrypt path/to/image.png "Your secret message" "your-password"
```

To auto-generate a password:

```bash
python client.py encrypt path/to/image.png "Your secret message" --auto-generate
```

### Hiding a Message in an Audio File

```bash
python client.py encrypt path/to/audio.mp3 "Your secret message" "your-password" --type audio
```

### Extracting a Message from an Image

```bash
python client.py decrypt path/to/stego_image.png "your-password"
```

### Extracting a Message from an Audio File

```bash
python client.py decrypt path/to/stego_audio.wav "your-password" --type audio
```

## Working with the API

For developers who want to integrate steganography into their applications, the API provides programmatic access to all features.

### API Endpoints Overview

- `GET /api/health`: Check API health
- `GET /api/capabilities`: View API capabilities
- `POST /api/encrypt`: Hide encrypted data in a file
- `POST /api/decrypt`: Extract and decrypt hidden data
- `GET /api/download/{filename}`: Download a processed file

### Example: API Integration in Python

```python
import requests

# Base URL for the API
API_URL = "http://localhost:8080/api"

# Encrypt and hide a message
def encrypt_message(file_path, message, password=None, auto_generate=False):
    url = f"{API_URL}/encrypt"
    
    # Prepare the file
    files = {'file': open(file_path, 'rb')}
    
    # Prepare the form data
    data = {
        'message': message,
        'media_type': 'image'  # or 'audio'
    }
    
    if auto_generate:
        data['auto_generate'] = 'true'
    elif password:
        data['password'] = password
    
    # Send the request
    response = requests.post(url, files=files, data=data)
    
    # Check if successful
    if response.status_code == 200:
        result = response.json()
        if result['status'] == 'success':
            # Download the file
            download_url = f"{API_URL}/download/{result['output_filename']}"
            download_response = requests.get(download_url)
            
            # Save the file
            with open(result['output_filename'], 'wb') as f:
                f.write(download_response.content)
            
            return {
                'success': True,
                'filename': result['output_filename'],
                'password': result.get('auto_generated_password')
            }
    
    return {'success': False, 'error': response.text}

# Extract and decrypt a message
def decrypt_message(file_path, password=None):
    url = f"{API_URL}/decrypt"
    
    # Prepare the file
    files = {'file': open(file_path, 'rb')}
    
    # Prepare the form data
    data = {
        'media_type': 'image'  # or 'audio'
    }
    
    if password:
        data['password'] = password
    
    # Send the request
    response = requests.post(url, files=files, data=data)
    
    # Check if successful
    if response.status_code == 200:
        result = response.json()
        if result['status'] == 'success':
            return {
                'success': True,
                'message': result['message'],
                'password_found': result.get('password_found', False),
                'used_password': result.get('used_password')
            }
    
    return {'success': False, 'error': response.text}
```

## Tips for Best Results

### Image Steganography

1. **Use Lossless Formats**: PNG, BMP, and GIF files work best for steganography
2. **Avoid JPEG**: JPEG compression can destroy hidden data
3. **Larger Images**: Bigger images can store more data
4. **Avoid Image Editing**: Editing a stego image may destroy the hidden data

### Audio Steganography

1. **Use WAV Format**: WAV files provide the most reliable results
2. **Higher Quality**: Higher bitrate audio can store more data
3. **Avoid Compression**: Don't convert processed WAV files to MP3 or other compressed formats
4. **Avoid Audio Editing**: Editing a stego audio file may destroy the hidden data

### Password Management

1. **Auto-Generated Passwords**: Use the auto-generate feature for maximum security
2. **Password Storage**: If you opt to store the password in the file, you won't need to remember it
3. **Secure Storage**: If you generate your own password, store it securely
4. **Password Length**: Longer passwords provide better security

## Troubleshooting

### Common Issues

#### "No file part" Error
- Ensure you've selected a file before submitting

#### "No valid encrypted data found" Error
- Verify the file contains hidden data
- Check if the file was modified after encryption
- Ensure you're using the correct password

#### "FFmpeg not found" Error
- Install FFmpeg and add it to your system PATH

#### Browser Doesn't Show Results
- Check your browser's console for errors
- Try using a different browser
- Clear your browser cache

### Getting Help

If you encounter issues not covered in this guide:

1. Check the detailed logs in the terminal where the server is running
2. Look for error messages in the browser console
3. Try with different files to isolate the issue
4. Check for updates to the tool

## Security Best Practices

1. **Use Strong Passwords**: Longer passwords with mixed characters are more secure
2. **Avoid Reusing Passwords**: Use different passwords for different files
3. **Secure Transfer**: Use secure channels to transfer your stego files
4. **Metadata**: Be aware that file metadata could reveal information about the file's creation
5. **Backup**: Keep backups of your important stego files

## Advanced Use Cases

### Batch Processing

For processing multiple files, you can create a simple script:

```python
import os
import subprocess

def process_directory(directory, message, password):
    for filename in os.listdir(directory):
        if filename.endswith(('.png', '.bmp', '.gif')):
            file_path = os.path.join(directory, filename)
            print(f"Processing {file_path}...")
            subprocess.run([
                'python', 'client.py', 'encrypt', 
                file_path, message, password
            ])
    print("Processing complete!")

# Example usage
process_directory('images', 'This is a hidden message', 'SecurePassword123')
```

### Scheduled Operations

You can use task schedulers (cron on Linux/macOS, Task Scheduler on Windows) to run steganography operations at specific times:

```bash
# Example cron job to encrypt a daily backup message
0 0 * * * /path/to/python /path/to/client.py encrypt /path/to/template.png "$(date) - Daily backup completed" "SecurePassword123" > /path/to/log.txt
```

## Overview
This guide provides comprehensive documentation for the steganography tool, which allows users to hide encrypted messages within media files (images and audio) using advanced compression and encryption techniques.

## Features
- Message compression using zlib (DEFLATE) with maximum compression level
- AES-256 encryption for secure message protection
- Support for multiple image formats (PNG, JPG, JPEG, BMP, GIF)
- Support for audio files (WAV, with automatic conversion for other formats)
- Automatic password generation and storage
- Lossless steganography using LSB technique

## Technical Details

### Compression
The tool uses zlib's DEFLATE algorithm with maximum compression level (9) to minimize the size of messages before encryption. This allows for:
- More efficient storage in carrier files
- Reduced impact on carrier file quality
- Increased capacity for hidden messages
- Automatic compression and decompression

### Encryption
// ... existing code ... 