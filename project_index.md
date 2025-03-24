# Steganography Project Documentation Index

Welcome to the comprehensive documentation for the Steganography Project. This index provides a guide to all documentation files available in this project.

## Core Documentation

| Document | Description |
|----------|-------------|
| [README.md](README.md) | Project overview, quick start guide, and basic information about the steganography application. |
| [documentation.md](documentation.md) | Comprehensive documentation covering functionality, installation, usage, API endpoints, and troubleshooting. |
| [documentation_guide.md](documentation_guide.md) | Detailed user guide focusing on practical usage, with step-by-step instructions for hiding and extracting messages in media files. |

## Technical References

| Document | Description |
|----------|-------------|
| [api_reference.md](api_reference.md) | Complete API reference with detailed information about endpoints, request parameters, response structures, and code examples. |
| [encryption_decryption_process.md](encryption_decryption_process.md) | Detailed technical explanation of the complete encryption, compression and steganography process with diagrams and implementation details. |
| [troubleshooting_guide.md](troubleshooting_guide.md) | Solutions for common issues encountered during installation, encryption, decryption, and when using different media types. |
| [security_practices.md](security_practices.md) | Best practices for securing your steganography usage, including password management, operational security, and threat modeling. |
| [deployment_guide.md](deployment_guide.md) | Instructions for deploying the application in various environments including local, production, Docker, and cloud platforms. |

## Diagrams and Architecture

The application architecture follows a client-server model:

```
┌─────────────┐     HTTP     ┌──────────────┐
│ Web Browser ├───Requests───┤ Flask Server │
└─────────────┘              └───────┬──────┘
                                     │
┌─────────────┐                      │
│ Command Line├───API Calls──────────┤
│   Client    │                      │
└─────────────┘                      ▼
                             ┌──────────────┐
                             │ Steganography│
                             │    Engine    │
                             └──────────────┘
```

## Getting Started

If you're new to the project, we recommend starting with the following documentation sequence:

1. First, read the [README.md](README.md) for a quick overview
2. Then review the [documentation_guide.md](documentation_guide.md) for practical usage instructions
3. Refer to [api_reference.md](api_reference.md) if you're integrating with the API
4. Consult [troubleshooting_guide.md](troubleshooting_guide.md) if you encounter any issues

## Quick Links to Common Tasks

- **Installation**: [README.md](README.md) → Installation section
- **Hiding a message in an image**: [documentation_guide.md](documentation_guide.md) → Web Interface section
- **Extracting a hidden message**: [documentation_guide.md](documentation_guide.md) → Decryption section
- **Using the command line**: [documentation_guide.md](documentation_guide.md) → Command Line Operations section
- **API integration**: [api_reference.md](api_reference.md)
- **Secure usage**: [security_practices.md](security_practices.md)
- **Deployment options**: [deployment_guide.md](deployment_guide.md)

## Maintenance and Support

The documentation is maintained alongside the codebase. If you find any inaccuracies or have suggestions for improvements, please submit an issue or a pull request to the project repository.

## Core Components

### Utility Module (utils.py)
- **Steganography functions**: Image and audio embedding/extraction
- **Compression functions**: zlib-based message compression/decompression
- **Encryption functions**: AES-256 and XOR encryption
- **Media conversion**: Format conversion for images and audio
- **Password utilities**: Generation and handling

### API Server (api.py)
- **Web server**: Flask-based HTTP endpoints
- **REST API**: Encryption, decryption, and utility endpoints
- **File handling**: Upload, download, and processing logic
- **Error handling**: Consistent error responses 