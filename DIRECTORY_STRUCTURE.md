# Directory Structure - Steganography System

## 📁 Cleaned and Organized Structure

```
crypt/
├── 📄 Core Application Files
│   ├── api.py                      # Flask API server (main entry point)
│   ├── utils.py                    # Core utility functions and services
│   ├── client.py                   # Command-line API client
│   └── setup.py                    # Package setup configuration
│
├── 🌐 Web Interface
│   ├── templates/                  # HTML templates
│   │   ├── index.html             # Main web interface
│   │   ├── sign-in.html           # Authentication page
│   │   └── sign-up.html           # Registration page
│   └── static/                     # Web assets
│       ├── css/                   # Stylesheets
│       ├── js/                    # JavaScript files
│       └── img/                   # Images and icons
│
├── 🧪 Testing
│   └── tests/                      # Test suite
│       ├── test_api.py            # API endpoint tests
│       ├── test_utils.py          # Utility function tests
│       ├── conftest.py            # Test configuration
│       └── __init__.py            # Test package init
│
├── 📚 Documentation
│   └── docs/                       # Comprehensive documentation
│       ├── README.md              # Documentation overview
│       ├── system_architecture.md # UML system diagrams
│       ├── api_diagrams.md        # API flow diagrams
│       ├── data_models.md         # Data structure diagrams
│       ├── api_reference_detailed.md # API specifications
│       ├── utils_methods.md       # Utility documentation
│       ├── steganography_process.md # Technical details
│       ├── deployment_guide.md    # Production deployment
│       ├── security_practices.md  # Security guidelines
│       ├── troubleshooting_guide.md # Issue resolution
│       └── project_index.md       # Project organization
│
├── 💾 Runtime Directories
│   ├── uploads/                    # Temporary file uploads
│   ├── output/                     # Processed file outputs
│   └── .venv/                      # Python virtual environment
│
├── ⚙️ Configuration Files
│   ├── requirements.txt            # Production dependencies
│   ├── requirements-dev.txt        # Development dependencies
│   ├── .gitignore                  # Git ignore rules
│   └── README.md                   # Project overview
│
├── 📋 Project Management
│   ├── LICENSE                     # MIT License
│   ├── CONTRIBUTING.md             # Contribution guidelines
│   ├── SECURITY.md                 # Security policy
│   └── DIRECTORY_STRUCTURE.md      # This file
│
└── 🔧 Development Tools
    ├── .git/                       # Git repository
    └── .github/                    # GitHub workflows and templates
```

## 🗑️ Removed Files and Directories

The following files were removed during cleanup to streamline the project:

### Removed Files
- `main.py` - Redundant with api.py as main entry point
- `encrypt_gui.py` - GUI interface removed (web interface preferred)
- `decrypt_gui.py` - GUI interface removed (web interface preferred)
- `test_qr.py` - Standalone test file (moved to organized test suite)
- `conftest.py` - Duplicate file (kept in tests/ directory)
- `stegano.db` - Database file (system doesn't use persistent DB)
- `security.log` - Log file (not needed for core functionality)

### Removed Directories
- `archived_docs/` - Outdated documentation (consolidated into docs/)
- `__pycache__/` - Python cache directories
- `.pytest_cache/` - Test cache directories

### Reorganized Files
- All documentation moved to `docs/` directory
- Deployment and troubleshooting guides organized
- Project structure documentation centralized

## 🎯 Key Benefits of New Structure

### 1. **Clear Separation of Concerns**
- Core application logic in root directory
- Documentation centralized in `docs/`
- Tests organized in `tests/`
- Web assets in `templates/` and `static/`

### 2. **Improved Maintainability**
- Single entry point (`api.py`)
- Consolidated utility functions (`utils.py`)
- Organized test suite
- Comprehensive documentation

### 3. **Better Developer Experience**
- Clear project navigation
- Comprehensive UML diagrams
- Detailed API documentation
- Troubleshooting guides

### 4. **Production Ready**
- Clean deployment structure
- Security best practices documented
- Performance optimization guides
- Monitoring and logging guidelines

## 📊 File Statistics

| Category | Files | Total Size |
|----------|-------|------------|
| Core Application | 3 | ~78KB |
| Web Interface | 3 templates + assets | ~50KB |
| Documentation | 11 files | ~100KB |
| Tests | 4 files | ~15KB |
| Configuration | 6 files | ~15KB |
| **Total** | **~27 files** | **~258KB** |

## 🚀 Quick Start Guide

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Application**
   ```bash
   python api.py
   ```

3. **Access the Interface**
   - Web UI: http://localhost:8080
   - API: http://localhost:8080/api/
   - Health Check: http://localhost:8080/api/health

4. **Run Tests**
   ```bash
   python -m pytest tests/
   ```

5. **Read Documentation**
   - Start with `docs/README.md`
   - Review `docs/system_architecture.md` for technical details

## 📈 UML Diagrams Available

The documentation includes comprehensive UML diagrams:

1. **System Architecture** (`docs/system_architecture.md`)
   - Component diagrams
   - Class diagrams
   - Deployment diagrams
   - State diagrams
   - Activity diagrams

2. **API Documentation** (`docs/api_diagrams.md`)
   - Sequence diagrams
   - Request/response flows
   - Authentication flows
   - Error handling flows

3. **Data Models** (`docs/data_models.md`)
   - Data structure diagrams
   - Entity relationships
   - File processing flows
   - Configuration models

All diagrams use proper Mermaid.js syntax with correct arrow relationships and styling.

---

*This structure provides a clean, maintainable, and well-documented codebase ready for development and production deployment.* 