# Steganography System Documentation

This directory contains comprehensive documentation for the steganography system, including detailed UML diagrams and architectural specifications.

## 📋 Documentation Overview

### 🏗️ Architecture Documentation
- **[System Architecture](system_architecture.md)** - Complete system overview with component diagrams, class diagrams, and deployment architecture
- **[API Diagrams](api_diagrams.md)** - Detailed API endpoint documentation with sequence diagrams and request/response flows
- **[Data Models](data_models.md)** - Data structures, relationships, and validation rules

### 📚 Additional Documentation
- **[API Reference](api_reference_detailed.md)** - Detailed API endpoint specifications
- **[Utils Methods](utils_methods.md)** - Core utility functions documentation
- **[Steganography Process](steganography_process.md)** - Technical implementation details
- **[Deployment Guide](deployment_guide.md)** - Production deployment instructions
- **[Security Practices](security_practices.md)** - Security implementation guidelines
- **[Troubleshooting Guide](troubleshooting_guide.md)** - Common issues and solutions
- **[Project Index](project_index.md)** - Project structure and file organization

## 🎯 Quick Navigation

### For Developers
1. Start with [System Architecture](system_architecture.md) for overall understanding
2. Review [API Diagrams](api_diagrams.md) for API implementation details
3. Check [Data Models](data_models.md) for data structure specifications
4. Refer to [Utils Methods](utils_methods.md) for implementation details

### For DevOps/Deployment
1. Follow [Deployment Guide](deployment_guide.md) for production setup
2. Implement [Security Practices](security_practices.md) recommendations
3. Use [Troubleshooting Guide](troubleshooting_guide.md) for issue resolution

### For API Users
1. Review [API Reference](api_reference_detailed.md) for endpoint specifications
2. Check [API Diagrams](api_diagrams.md) for request/response flows

## 🔧 System Components

### Core Components
```
├── api.py              # Flask API server and routes
├── utils.py            # Core utility functions and services
├── client.py           # Command-line API client
├── templates/          # Web interface templates
├── static/             # Web assets (CSS, JS, images)
├── tests/              # Test suite
├── uploads/            # Temporary file uploads
└── output/             # Processed file outputs
```

### Key Features
- **Multi-format Support**: Images (PNG, JPG, BMP, GIF) and Audio (WAV, MP3, OGG, FLAC)
- **Advanced Encryption**: AES-256-CBC with PBKDF2 key derivation
- **Smart Compression**: Automatic zlib compression with size optimization
- **QR Code Integration**: Generate and process encrypted QR codes
- **Web Interface**: Modern, responsive web UI
- **REST API**: Complete RESTful API for integration
- **CLI Client**: Command-line interface for automation

## 📊 UML Diagram Types

### 1. Structural Diagrams
- **Component Diagram**: System components and their relationships
- **Class Diagram**: Object-oriented design and class relationships
- **Deployment Diagram**: Production deployment architecture

### 2. Behavioral Diagrams
- **Sequence Diagram**: Process flows and interactions
- **Activity Diagram**: Business logic and decision flows
- **State Diagram**: Object state transitions

### 3. Data Flow Diagrams
- **Data Model Diagrams**: Database and data structure relationships
- **API Flow Diagrams**: Request/response data flows
- **Processing Pipeline**: Data transformation stages

## 🚀 Getting Started

### Prerequisites
```bash
# Python 3.8+
pip install -r requirements.txt

# Optional: FFmpeg for audio conversion
# Windows: Download from https://ffmpeg.org/
# Linux: sudo apt-get install ffmpeg
# macOS: brew install ffmpeg
```

### Quick Start
```bash
# Start the API server
python api.py

# Use the web interface
# Open http://localhost:8080 in your browser

# Or use the CLI client
python client.py encrypt image.png "secret message" "password"
python client.py decrypt stego_image.png "password"
```

## 🔒 Security Features

- **AES-256-CBC Encryption**: Industry-standard encryption
- **PBKDF2 Key Derivation**: 100,000 iterations for key strengthening
- **Secure File Handling**: Automatic cleanup and secure filename generation
- **Authentication**: Token-based API authentication
- **Input Validation**: Comprehensive input sanitization
- **Rate Limiting**: Protection against abuse

## 📈 Performance Characteristics

### Compression Efficiency
- **Text Messages**: 30-70% size reduction
- **Repetitive Content**: Up to 95% compression
- **Binary Data**: Variable compression based on entropy

### Processing Speed
- **Image Processing**: ~1-5 seconds for typical images
- **Audio Processing**: ~2-10 seconds depending on file size
- **QR Code Generation**: ~0.5-2 seconds

### Capacity Limits
- **Images**: 3 bits per pixel (RGB channels)
- **Audio**: 1 bit per sample
- **File Size**: Maximum 64MB upload limit

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/test_api.py
python -m pytest tests/test_utils.py

# Run with coverage
python -m pytest --cov=. tests/
```

## 📝 API Endpoints Summary

| Endpoint | Method | Purpose | Auth Required |
|----------|--------|---------|---------------|
| `/api/health` | GET | Health check | No |
| `/api/capabilities` | GET | System capabilities | No |
| `/api/encrypt` | POST | Hide message in media | Yes |
| `/api/decrypt` | POST | Extract message from media | Yes |
| `/api/generate-qr` | POST | Generate QR code | Yes |
| `/api/encrypt-qr` | POST | Create encrypted QR code | Yes |
| `/api/decrypt-qr` | POST | Decrypt QR code message | Yes |
| `/api/download/:filename` | GET | Download processed file | Yes |

## 🤝 Contributing

1. Review the [System Architecture](system_architecture.md) to understand the codebase
2. Check existing [API Diagrams](api_diagrams.md) before making changes
3. Update relevant UML diagrams when modifying system structure
4. Follow the patterns established in [Data Models](data_models.md)
5. Add tests for new functionality

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🆘 Support

- **Documentation**: Review the relevant documentation files in this directory
- **Troubleshooting**: Check [Troubleshooting Guide](troubleshooting_guide.md)
- **Security Issues**: Follow [Security Practices](security_practices.md)
- **Deployment**: Use [Deployment Guide](deployment_guide.md)

---

*Last updated: May 2025* 