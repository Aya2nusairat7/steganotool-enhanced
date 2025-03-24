# Steganography Tool Documentation

This comprehensive documentation covers all aspects of the Steganography Tool, a versatile application for hiding encrypted messages in media files.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Architecture](#architecture)
5. [User Interfaces](#user-interfaces)
   - [Web Interface](#web-interface)
   - [Command-Line Interface](#command-line-interface)
   - [API](#api)
6. [Technical Details](#technical-details)
   - [Steganography Process](#steganography-process)
   - [Data Compression](#data-compression)
   - [Encryption Methods](#encryption-methods)
   - [Media Support](#media-support)
7. [API Reference](#api-reference)
8. [Usage Examples](#usage-examples)
9. [Advanced Topics](#advanced-topics)
10. [Troubleshooting](#troubleshooting)
11. [Security Considerations](#security-considerations)

## Introduction

The Steganography Tool is a secure application designed to hide encrypted messages within media files such as images and audio. By leveraging steganography techniques, the tool embeds data in ways that are undetectable to the casual observer. This provides an additional layer of security beyond encryption alone, as the very existence of the message remains hidden.

The tool supports multiple interfaces including a modern web UI, a command-line interface, and a RESTful API, making it suitable for a wide range of use cases from personal security to application integration.

## Features

### Core Features

- **Image Steganography**: Hide data in image files (PNG, BMP, GIF)
- **Audio Steganography**: Hide data in audio files (WAV)
- **Strong Encryption**: AES-256 encryption for message security
- **Format Conversion**: Automatic conversion of supported formats
- **Password Management**: Auto-generation and secure storage of passwords
- **Multiple Interfaces**: Web UI, command-line client, and RESTful API

### Security Features

- **End-to-end Encryption**: Messages are encrypted before being hidden
- **Auto-generated Passwords**: Option to use cryptographically strong random passwords
- **Password Embedding**: Passwords can be securely stored within the media
- **XOR Fallback**: Alternative encryption for small messages

### Usability Features

- **Modern Web Interface**: User-friendly design with responsive layout
- **Format Detection**: Automatic media type detection
- **Comprehensive API**: Full access to all features programmatically
- **Detailed Feedback**: Clear status messages and error reporting

## Installation

### Prerequisites

- Python 3.7 or higher
- FFmpeg (for audio conversion)
- Modern web browser (for web interface)

### Step 1: Clone or Download the Repository

```bash
git clone https://github.com/yourusername/steganography-tool.git
cd steganography-tool
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` file includes:

```
flask==2.0.1
Pillow==9.0.0
numpy==1.21.0
pycryptodome==3.11.0
requests==2.27.1
opencv-python==4.5.5.64
```

### Step 3: Install FFmpeg (for audio processing)

**Windows**:
- Download from [FFmpeg.org](https://ffmpeg.org/download.html)
- Add the `bin` folder to your PATH environment variable

**macOS**:
```bash
brew install ffmpeg
```

**Linux (Debian/Ubuntu)**:
```bash
sudo apt update
sudo apt install ffmpeg
```

### Step 4: Run the Application

Start the Flask server:

```bash
python api.py
```

By default, the server will run on `http://localhost:8080`

## Architecture

The Steganography Tool is built with a modular architecture consisting of several key components:

### Component Overview

1. **Core Utilities (`utils.py`)**: Contains the fundamental functions for steganography, encryption, and format conversion.

2. **API Server (`api.py`)**: Provides RESTful endpoints for all functionality and serves the web interface.

3. **Command-line Client (`client.py`)**: Provides a terminal interface to interact with the API.

4. **Web Interface**: HTML/CSS/JavaScript frontend for user-friendly interaction.

### Data Flow

1. **Encryption Process**:
   - User input (message, password) → Encryption → Data preparation → Media hiding → Output file

2. **Decryption Process**:
   - Input file → Data extraction → Password extraction (if available) → Decryption → Output message

### System Requirements

- **Minimum**: 
  - 2GB RAM
  - 500MB free disk space
  - Python 3.7+
  
- **Recommended**:
  - 4GB RAM
  - 1GB free disk space
  - Python 3.9+
  - FFmpeg (latest version)

## User Interfaces

The tool provides three distinct interfaces to accommodate different use cases and preferences.

### Web Interface

The web interface provides a modern, user-friendly way to interact with the steganography tool.

#### Features

- **Responsive Design**: Works on desktop and mobile devices
- **Intuitive Forms**: Separate sections for encryption and decryption
- **Real-time Feedback**: Immediate results and error messages
- **Visual Elements**: Icons and visual cues for better user experience
- **API Documentation**: Built-in reference for developers

#### Accessing the Web Interface

1. Start the server: `python api.py`
2. Open a web browser and navigate to `http://localhost:8080`

### Command-Line Interface

The command-line interface (CLI) allows for quick operations and automation via scripts.

#### Available Commands

- `health`: Check if the API server is running
- `capabilities`: List the capabilities of the API
- `encrypt`: Encrypt and hide a message in a media file
- `decrypt`: Extract and decrypt a message from a media file

#### Basic Usage

```bash
# Check API health
python client.py health

# Encrypt a message in an image
python client.py encrypt path/to/image.png "Secret message" "password"

# Decrypt a message from an image
python client.py decrypt path/to/stego_image.png "password"

# Encrypt a message in an audio file
python client.py encrypt path/to/audio.mp3 "Secret message" "password" --type audio
```

### API

The RESTful API allows for integration with other applications and services.

#### Key Endpoints

- `GET /api/health`: Check API health
- `GET /api/capabilities`: Get API capabilities
- `POST /api/encrypt`: Encrypt and hide a message
- `POST /api/decrypt`: Extract and decrypt a message
- `GET /api/download/{filename}`: Download a processed file

## Technical Details

### Steganography Process

The tool implements several steganography techniques depending on the media type:

#### Image Steganography

For images, the tool uses the **Least Significant Bit (LSB)** technique:

1. Each pixel in an image consists of color channels (RGB)
2. The least significant bit of each color value is modified to store data
3. This creates imperceptible changes to the image
4. For an RGB image, up to 3 bits of data can be stored per pixel

#### Audio Steganography

For audio files, the tool implements:

1. LSB encoding in audio samples
2. Data is spread across audio frames
3. Human ear cannot detect the slight modifications

### Data Compression

Before encryption, the tool applies compression to the message data:

#### Compression Method
- Uses **zlib's DEFLATE algorithm** with maximum compression level (9)
- Applied to all messages regardless of size
- Significantly reduces the amount of data needed to be hidden
- Allows hiding more information in the same carrier file
- Improves security by making the hidden data more compact

#### Compression Process
1. Raw message is converted to bytes (if not already)
2. zlib compression is applied with level 9 (maximum)
3. Compressed data is then passed to the encryption module
4. During extraction, the reverse process automatically decompresses the data

#### Compression Benefits
- **Size Reduction**: Typically achieves 30-70% reduction for text messages
- **Capacity Increase**: Allows hiding larger messages in the same carrier file
- **Security Enhancement**: Compressed data has higher entropy, making statistical analysis harder
- **Performance**: Despite the additional processing step, compression often speeds up the overall process by reducing the amount of data to encrypt and hide

### Encryption Methods

The tool uses two primary encryption methods:

#### AES-256 Encryption

- Used for messages larger than 32 bytes
- Implements AES in CBC mode
- Uses PBKDF2 for key derivation
- Includes salt and IV in the encrypted data
- Applied to compressed message data

#### XOR Encryption

- Used for small messages (less than 32 bytes)
- Faster and simpler than AES
- Still provides adequate security for short messages
- Uses SHA-256 hash of the password as the XOR key
- Applied to compressed message data

### Media Support

#### Supported Image Formats

- **Input**: PNG, BMP, GIF, JPEG (converted to PNG)
- **Output**: PNG, BMP, GIF

#### Supported Audio Formats

- **Input**: WAV, MP3, OGG, FLAC, M4A, AAC (all converted to WAV)
- **Output**: WAV

## API Reference

### Health Check

**Endpoint**: `GET /api/health`

**Response**:
```json
{
  "status": "healthy"
}
```

### Get Capabilities

**Endpoint**: `GET /api/capabilities`

**Response**:
```json
{
  "image_steganography": true,
  "audio_steganography": true,
  "audio_conversion": true,
  "image_conversion": true
}
```

### Encrypt Message

**Endpoint**: `POST /api/encrypt`

**Form Parameters**:
- `file`: The media file (image or audio)
- `message`: The message to encrypt and hide
- `password`: The encryption password (optional if auto_generate is true)
- `auto_generate`: Whether to auto-generate a password (true/false)
- `media_type`: Either "image" or "audio"

**Response**:
```json
{
  "status": "success",
  "original_filename": "example.png",
  "output_filename": "stego_example.png",
  "file_size": 123456,
  "encrypted_size": 1024,
  "message_length": 255,
  "auto_generated": true,
  "auto_generated_password": "A3b!9^xK_lP2@dR5",
  "download_url": "/api/download/stego_example.png",
  "media_type": "image"
}
```

### Decrypt Message

**Endpoint**: `POST /api/decrypt`

**Form Parameters**:
- `file`: The media file containing hidden data
- `password`: The decryption password (optional if embedded in file)
- `media_type`: Either "image" or "audio"

**Response**:
```json
{
  "status": "success",
  "filename": "stego_example.png",
  "message": "This is the decrypted secret message",
  "message_length": 36,
  "password_found": true,
  "used_password": "A3b!9^xK_lP2@dR5"
}
```

### Download File

**Endpoint**: `GET /api/download/{filename}`

**Response**: The file as an attachment

## Usage Examples

### Basic Usage

#### Web Interface

1. **Encrypting a Message**:
   - Open the web interface
   - Choose a media file in the "Encrypt & Hide" section
   - Enter your message
   - Choose to enter a password or auto-generate one
   - Click "Encrypt & Hide"
   - Download the resulting file

2. **Decrypting a Message**:
   - Open the web interface
   - Upload your steganography file in the "Extract & Decrypt" section
   - Enter the password (if not embedded in the file)
   - Click "Extract & Decrypt"
   - View the decrypted message

#### Command Line

1. **Encrypting a Message**:
   ```bash
   python client.py encrypt image.png "This is a secret message" "MyPassword123"
   ```

2. **Decrypting a Message**:
   ```bash
   python client.py decrypt stego_image.png "MyPassword123"
   ```

### Advanced Usage

#### Auto-Generated Passwords

```bash
python client.py encrypt image.png "This is a secret message" --auto-generate
```

#### API Integration Example (Python)

```python
import requests

# Encrypt a message
def encrypt_message(file_path, message, password):
    url = "http://localhost:8080/api/encrypt"
    files = {'file': open(file_path, 'rb')}
    data = {
        'message': message,
        'password': password,
        'media_type': 'image'
    }
    
    response = requests.post(url, files=files, data=data)
    return response.json()

# Decrypt a message
def decrypt_message(file_path, password):
    url = "http://localhost:8080/api/decrypt"
    files = {'file': open(file_path, 'rb')}
    data = {
        'password': password,
        'media_type': 'image'
    }
    
    response = requests.post(url, files=files, data=data)
    return response.json()
```

## Advanced Topics

### Custom Encryption Settings

While the default encryption settings are secure, advanced users can modify `utils.py` to adjust:

- Key derivation iterations (default: 100,000)
- AES mode (default: CBC)
- Padding scheme (default: PKCS7)

### Batch Processing

The command-line client can be extended for batch processing with a script like:

```python
import os
import subprocess

def batch_encrypt(directory, message, password):
    for filename in os.listdir(directory):
        if filename.endswith(('.png', '.bmp', '.gif')):
            file_path = os.path.join(directory, filename)
            subprocess.run([
                'python', 'client.py', 'encrypt', 
                file_path, message, password
            ])
```

### Integration with Other Systems

The API can be integrated with:

- Web applications
- Mobile apps
- Desktop applications
- Workflow automation tools

## Troubleshooting

### Common Issues

#### "FFmpeg not found" Error

**Solution**: Ensure FFmpeg is installed and in your system PATH.

#### "No valid encrypted data found" Error

**Solutions**:
- Verify you're using the correct password
- Check that the file contains hidden data
- Ensure the file hasn't been modified or compressed

#### "Error during conversion" for Audio Files

**Solution**: Install FFmpeg and ensure it's in your system PATH.

#### Browser Console Errors

**Solutions**:
- Clear browser cache
- Update your browser
- Check for JavaScript errors in the console

### Debugging Tips

1. Run the Flask app in debug mode (default)
2. Check terminal output for detailed error messages
3. For API issues, examine the raw response data
4. For steganography problems, try with different files

## Security Considerations

### Strengths

- **Multiple Security Layers**: Encryption + steganography
- **Strong Encryption**: AES-256 with proper key derivation
- **Password Management**: Option for auto-generated strong passwords

### Limitations

- **File Size Increase**: Steganography slightly increases file size
- **Format Limitations**: Best with lossless formats (PNG, WAV)
- **Compression Vulnerability**: Compression can destroy hidden data

### Best Practices

1. **Use Lossless Formats**: Prefer PNG for images and WAV for audio
2. **Strong Passwords**: Use auto-generated passwords when possible
3. **Secure Transfer**: Use secure channels to transfer steganographic files
4. **Original Files**: Keep original files separate from steganographic copies
5. **Password Protection**: Store passwords securely, separate from files 