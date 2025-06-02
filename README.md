# SteganoTool

<p align="center">
  <img src="static/img/logo.png" alt="SteganoTool Logo" width="200"/>
</p>

<p align="center">
  A modern steganography tool for hiding secret messages in images and audio files
</p>

<p align="center">
  <img src="https://github.com/YazeedSalem0/steganotool-enhanced/actions/workflows/python-tests.yml/badge.svg" alt="Tests Status"/>
  <a href="https://codecov.io/gh/YazeedSalem0/steganotool-enhanced">
    <img src="https://codecov.io/gh/YazeedSalem0/steganotool-enhanced/branch/main/graph/badge.svg" alt="Coverage Status"/>
  </a>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#how-it-works">How It Works</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>

## Features

- **Multiple Media Types**: Hide messages in various media types including images (PNG, JPG, BMP) and audio files (WAV)
- **Data Compression**: Advanced compression techniques that minimize message size before encryption
- **Strong Encryption**: AES-256 encryption to protect your hidden messages
- **Password Management**: Option to auto-generate secure passwords or use your own
- **Intuitive UI**: Modern web interface for easy message hiding and extraction
- **Visual Workflow**: Interactive visualizations that help you understand the steganography process
- **QR Code Steganography**: NEW!
  - Generate QR codes with data
  - Hide encrypted messages in QR codes
  - Different QR styles: standard, fancy, embedded
  - Optional background image for QR codes
  - Automatic password embedding in QR codes

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### Setup

1. Clone the repository:
  ```bash
   git clone https://github.com/YazeedSalem0/steganotool-enhanced.git
   cd steganotool-enhanced
  ```

2. Install the required dependencies:
  ```

## Usage

### Starting the Application

1. Start the application server:
```bash
python api.py
```

2. Open your web browser and navigate to:
   ```
   http://localhost:8080
   ```

### Step-by-Step Usage Guide

#### Hiding a Message in an Image

1. **Select an Image**: From the main page, click "Encrypt" and upload an image file (PNG, JPG, or BMP)
2. **Enter Your Message**: Type your secret message in the text area
3. **Password Options**: Either enter your own password or select "Auto-generate password"
4. **Process**: Click "Encrypt" to process your image and hide the message
5. **Download**: Once processing is complete, download your steganographic image

#### Extracting a Hidden Message

1. **Upload Stego File**: From the main page, click "Decrypt" and upload the steganographic image
2. **Password Entry**: If the password wasn't embedded in the file, enter it in the password field
3. **Extract**: Click "Decrypt" to extract and decrypt the hidden message
4. **View Results**: The decoded message will be displayed on the screen

### Test Samples

You can use these test samples to try out the application:

#### Sample 1: Basic Text Hiding

1. Use any JPG or PNG image as your carrier file
2. Use this sample text message:
   ```
   This is a secret message that will be hidden in the image using steganography.
   The message is encrypted with AES-256 before being hidden in the image.
   ```
3. Use password: `test123password`
4. Compare the original and resulting images - they should look visually identical

#### Sample 2: Image Capacity Test

1. Use a 1024x768 PNG image (approximately 2MB)
2. This size of image can hide approximately 150KB of text (about 25,000 words)
3. Use auto-generated password option for convenience
4. The final image will be a PNG regardless of input format

#### Sample 3: Command Line Usage

For those who prefer command line:

```bash
# Encrypt a message in an image
python client.py encrypt --image path/to/image.jpg --message "Secret message" --password "your-password" --output stego-image.png

# Decrypt a message from an image
python client.py decrypt --image path/to/stego-image.png --password "your-password"
```

### Tips for Best Results

- PNG files work best as carrier files since they are lossless
- Larger images can store more data
- The auto-generated password option is recommended for maximum security
- Always download and save the output image immediately - don't take screenshots of it
- Remember that modifying the steganographic image (resizing, cropping, color adjustments) will likely destroy the hidden message

## How It Works

SteganoTool uses the following workflow for hiding and extracting messages:

### Encryption Process

1. **Select a carrier file**: Choose an image or audio file to hide your message in
2. **Enter your secret message**: Type or paste the confidential message to be hidden
3. **Compression process**: The message is compressed using zlib to minimize size
4. **Provide a password**: Enter a strong password or use the auto-generate feature
5. **Encryption process**: The compressed message is encrypted using AES-256 encryption
   - For short messages (<32 bytes), a simpler XOR encryption is used
   - For longer messages, AES-256 encryption in CBC mode with a random IV is used
   - The password is used to derive a secure encryption key using PBKDF2
6. **Steganography process**: The encrypted message is hidden in the carrier file
   - For images: Uses the Least Significant Bit (LSB) technique to modify pixel data
   - The data is spread across color channels (RGB) to minimize visual impact
   - For audio: Embeds data in frequency domains or silent sections
7. **Embedding password**: The password is optionally embedded in the file after a marker byte (0x01)
8. **Download stego file**: The resulting file with hidden data is available for download

### Decryption Process

1. **Upload stego file**: Upload the file containing the hidden message
2. **Extraction process**: The system extracts the hidden data from the carrier file
   - For images: The LSB data is extracted and reconstructed
   - For audio: The embedded data is extracted from frequency or time domains
3. **Password retrieval**: The system checks for an embedded password after marker byte 0x01
   - If found, it's used automatically
   - If not found, the user must provide the password
4. **Decryption process**: 
   - The system first attempts XOR decryption for short messages
   - If XOR decryption doesn't yield valid UTF-8, AES decryption is used
   - The password is used to derive the same encryption key using PBKDF2
5. **Decompression process**: The decrypted data is decompressed using zlib
6. **View secret message**: The original message is displayed to the user

### Technical Implementation

- **Image Steganography**: Uses Python's Pillow library to manipulate image data
- **Audio Steganography**: Uses audio processing libraries for WAV manipulation
- **Encryption**: Implemented using PyCryptodome for AES operations
- **Web Interface**: Built with Flask to provide a user-friendly experience
- **Format Conversion**: Converts various image formats to PNG for consistent processing

## Contributing

We welcome contributions from the community. If you're interested in contributing, please follow our [contribution guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Running Tests

The project includes comprehensive tests to ensure functionality. Here's how to run them:

### Prerequisites

Make sure you have installed the development dependencies:
```bash
pip install -r requirements-dev.txt
pip install pytest pytest-cov
```

### Running Basic Tests

To run all tests:
```bash
pytest
```

For more detailed output:
```bash
pytest -v
```

### Running Specific Tests

To run only the API tests:
```bash
pytest tests/test_api.py -v
```

To run only the utility tests:
```bash
pytest tests/test_utils.py -v
```

### Test Coverage Reports

Generate a terminal coverage report:
```bash
pytest --cov=. --cov-report=term
```

Generate an HTML coverage report:
```bash
pytest --cov=. --cov-report=html
```

This creates a `htmlcov` directory with HTML files showing coverage details. Open `htmlcov/index.html` in your browser to view.

Generate an XML coverage report for CI tools:
```bash
pytest --cov=. --cov-report=xml
```

### Test Structure

- **test_api.py**: Tests for the web API endpoints and request handling
- **test_utils.py**: Tests for core utilities like encryption/decryption and steganography functions

### Continuous Integration

The project uses GitHub Actions for continuous integration, automatically running tests on every push and pull request to ensure code quality.

## API Endpoints

The application exposes the following API endpoints:

- `POST /api/encrypt` - Encrypt and hide a message in an image or audio file
- `POST /api/decrypt` - Extract and decrypt a message from an image or audio file
- `GET /api/download/<filename>` - Download a generated file
- `GET /api/capabilities` - Get information about supported features
- `POST /api/generate-qr` - Generate a QR code from data
- `POST /api/encrypt-qr` - Encrypt a message and generate a QR code containing it
- `POST /api/decrypt-qr` - Extract and decrypt a message from a QR code