# Steganography System

<p align="center">
  <img src="static/img/logo.png" alt="Steganography System Logo" width="200"/>
</p>

<p align="center">
  A modern, comprehensive steganography system for hiding secret messages in images, audio files, and QR codes
</p>

<p align="center">
  <img src="https://github.com/YazeedSalem0/steganotool-enhanced/actions/workflows/python-tests.yml/badge.svg" alt="Tests Status"/>
  <a href="https://codecov.io/gh/YazeedSalem0/steganotool-enhanced">
    <img src="https://codecov.io/gh/YazeedSalem0/steganotool-enhanced/branch/main/graph/badge.svg" alt="Coverage Status"/>
  </a>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#usage">Usage</a> •
  <a href="#api">API</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>

## 🚀 Features

### Core Capabilities
- **Multi-Format Support**: Images (PNG, JPG, BMP, GIF) and Audio (WAV, MP3, OGG, FLAC)
- **Advanced Encryption**: AES-256-CBC with PBKDF2 key derivation (100,000 iterations)
- **Smart Compression**: Automatic zlib compression with 30-95% size reduction
- **Password Management**: Auto-generate secure passwords or use custom ones
- **Password Embedding**: Automatic password embedding in steganographic files

### Interface Options
- **Modern Web UI**: Responsive, intuitive web interface
- **REST API**: Complete RESTful API for integration
- **CLI Client**: Command-line interface for automation
- **Comprehensive Documentation**: UML diagrams and detailed guides

### QR Code Integration
- **QR Generation**: Create QR codes with embedded data
- **QR Steganography**: Hide encrypted messages in QR codes
- **Multiple Styles**: Standard, fancy, and embedded background styles
- **Auto-Password**: Automatic password embedding in QR codes

### Security Features
- **Industry-Standard Encryption**: AES-256-CBC encryption
- **Secure Key Derivation**: PBKDF2 with salt and high iteration count
- **Input Validation**: Comprehensive sanitization and validation
- **Secure File Handling**: Automatic cleanup and secure naming
- **Authentication**: Token-based API authentication

## 📚 Documentation

Comprehensive documentation is available in the [`docs/`](docs/) directory:

### 🏗️ Architecture & Design
- **[System Architecture](docs/system_architecture.md)** - UML diagrams and system overview
- **[API Documentation](docs/api_diagrams.md)** - API flows and endpoint specifications
- **[Data Models](docs/data_models.md)** - Data structures and relationships

### 📖 User Guides
- **[Documentation Overview](docs/README.md)** - Complete documentation index
- **[API Reference](docs/api_reference_detailed.md)** - Detailed endpoint specifications
- **[Utils Methods](docs/utils_methods.md)** - Core utility functions
- **[Steganography Process](docs/steganography_process.md)** - Technical implementation

### 🔧 Operations
- **[Deployment Guide](docs/deployment_guide.md)** - Production deployment
- **[Security Practices](docs/security_practices.md)** - Security guidelines
- **[Troubleshooting](docs/troubleshooting_guide.md)** - Issue resolution
- **[Project Structure](docs/project_index.md)** - Codebase organization

## ⚡ Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YazeedSalem0/steganotool-enhanced.git
   cd steganotool-enhanced
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the application:**
   ```bash
   python api.py
   ```

4. **Access the interface:**
   - Web UI: http://localhost:8080
   - API: http://localhost:8080/api/
   - Health Check: http://localhost:8080/api/health

## 📋 Usage

### Web Interface

1. **Encrypt a Message:**
   - Upload an image or audio file
   - Enter your secret message
   - Choose password options (manual or auto-generate)
   - Download the steganographic file

2. **Decrypt a Message:**
   - Upload the steganographic file
   - Enter password (if not embedded)
   - View the extracted message

### Command Line Interface

```bash
# Encrypt a message
python client.py encrypt image.png "secret message" "password"

# Decrypt a message
python client.py decrypt stego_image.png "password"

# Generate QR code
python client.py qr-encrypt "secret message" "password"

# Decrypt QR code
python client.py qr-decrypt qr_code.png "password"
```

### API Usage

```bash
# Health check
curl http://localhost:8080/api/health

# Get capabilities
curl http://localhost:8080/api/capabilities

# Encrypt (requires authentication)
curl -X POST -H "Authorization: Bearer <token>" \
  -F "file=@image.png" \
  -F "message=secret message" \
  -F "password=mypassword" \
  http://localhost:8080/api/encrypt
```

## 🔧 API Endpoints

| Endpoint | Method | Purpose | Auth Required |
|----------|--------|---------|---------------|
| `/api/health` | GET | Health check | No |
| `/api/capabilities` | GET | System capabilities | No |
| `/api/auth/sign-in` | POST | User authentication | No |
| `/api/auth/sign-up` | POST | User registration | No |
| `/api/encrypt` | POST | Hide message in media | Yes |
| `/api/decrypt` | POST | Extract message from media | Yes |
| `/api/generate-qr` | POST | Generate QR code | Yes |
| `/api/encrypt-qr` | POST | Create encrypted QR code | Yes |
| `/api/decrypt-qr` | POST | Decrypt QR code message | Yes |
| `/api/download/:filename` | GET | Download processed file | Yes |

For detailed API documentation, see [API Reference](docs/api_reference_detailed.md).

## 🧪 Testing

### Run Tests
```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=. tests/

# Run specific tests
python -m pytest tests/test_api.py -v
python -m pytest tests/test_utils.py -v
```

### Test Coverage
```bash
# Generate HTML coverage report
python -m pytest --cov=. --cov-report=html tests/
# Open htmlcov/index.html in browser

# Generate terminal report
python -m pytest --cov=. --cov-report=term tests/
```

## 📊 Performance

### Compression Efficiency
- **Text Messages**: 30-70% size reduction
- **Repetitive Content**: Up to 95% compression
- **Binary Data**: Variable based on entropy

### Processing Speed
- **Image Processing**: 1-5 seconds for typical images
- **Audio Processing**: 2-10 seconds depending on size
- **QR Code Generation**: 0.5-2 seconds

### Capacity Limits
- **Images**: 3 bits per pixel (RGB channels)
- **Audio**: 1 bit per sample
- **File Size**: Maximum 64MB upload

## 🏗️ Architecture

The system follows a clean, modular architecture:

```
├── api.py              # Flask API server (main entry point)
├── utils.py            # Core utility functions and services
├── client.py           # Command-line API client
├── templates/          # Web interface templates
├── static/             # Web assets (CSS, JS, images)
├── tests/              # Comprehensive test suite
├── docs/               # Complete documentation with UML diagrams
├── uploads/            # Temporary file uploads
└── output/             # Processed file outputs
```

For detailed architecture documentation, see [System Architecture](docs/system_architecture.md).

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Install development dependencies: `pip install -r requirements-dev.txt`
4. Make your changes
5. Run tests: `python -m pytest tests/`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Start with [docs/README.md](docs/README.md)
- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Security**: See [SECURITY.md](SECURITY.md) for security policy
- **Troubleshooting**: Check [Troubleshooting Guide](docs/troubleshooting_guide.md)

## 🔒 Security

- AES-256-CBC encryption with PBKDF2 key derivation
- Secure random password generation
- Input validation and sanitization
- Automatic file cleanup
- Token-based authentication

For detailed security information, see [Security Practices](docs/security_practices.md).

---

**Built with ❤️ for secure communication**