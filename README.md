# SteganoTool

<p align="center">
  <img src="static/img/logo.png" alt="SteganoTool Logo" width="200"/>
</p>

<p align="center">
  A modern steganography tool for hiding secret messages in images and audio files
</p>

<p align="center">
  <img src="https://github.com/yourusername/steganotool/actions/workflows/python-tests.yml/badge.svg" alt="Tests Status"/>
  <a href="https://codecov.io/gh/yourusername/steganotool">
    <img src="https://codecov.io/gh/yourusername/steganotool/branch/main/graph/badge.svg" alt="Coverage Status"/>
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

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/steganotool.git
   cd steganotool
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the application:
   ```bash
   python api.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:8080
   ```

3. Use the web interface to:
   - Hide messages in images or audio files
   - Extract hidden messages from stego files
   - Explore the steganography process through interactive visualizations

## How It Works

SteganoTool uses the following workflow for hiding and extracting messages:

### Encryption Process
1. **Select a carrier file**: Choose an image or audio file
2. **Enter your secret message**: Type the confidential message
3. **Compression process**: The message is compressed to minimize size
4. **Provide a password**: Enter a strong password for encryption
5. **Encryption process**: The compressed message is encrypted using AES-256
6. **Steganography process**: The encrypted message is hidden in the carrier file
7. **Download stego file**: The resulting file contains the hidden message

### Decryption Process
1. **Upload stego file**: Upload the file containing the hidden message
2. **Extraction process**: The system extracts the hidden message
3. **Password retrieval**: Automatically extract or manually provide the password
4. **Decryption process**: Decrypt the hidden message using the password
5. **Decompression process**: Restore the original message from the decrypted data
6. **View secret message**: Display the original secret message

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

Please read our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Thanks to all contributors who have helped make this project better
- Special thanks to the open-source community for their invaluable resources and tools

## Running Tests

To run the tests, follow these steps:

1. Make sure you have installed the development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   pip install pytest pytest-cov
   ```

2. Ensure the required directories exist:
   ```bash
   mkdir -p uploads
   mkdir -p output
   ```

3. Run the tests using pytest:
   ```bash
   pytest
   ```

For more detailed test output, use:
```bash
pytest -v
```

To generate a coverage report:
```bash
# Terminal report
pytest --cov=. --cov-report=term

# HTML report (outputs to htmlcov/ directory)
pytest --cov=. --cov-report=html

# XML report for CI tools
pytest --cov=. --cov-report=xml
```

The coverage reports provide insights into which parts of the code are being tested and which parts need more test coverage. 