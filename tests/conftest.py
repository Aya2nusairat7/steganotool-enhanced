import pytest
import sys
import os
from unittest.mock import MagicMock

# Mock PyQt5 modules for CI testing environment
# This prevents issues with display/GUI when running in headless CI
try:
    import PyQt5
except ImportError:
    # If PyQt5 is not available, mock it
    sys.modules['PyQt5'] = MagicMock()
    sys.modules['PyQt5.QtCore'] = MagicMock()
    sys.modules['PyQt5.QtGui'] = MagicMock()
    sys.modules['PyQt5.QtWidgets'] = MagicMock()

# Fixture for creating temporary directories for testing
@pytest.fixture
def temp_dir(tmp_path):
    """Provides a temporary directory for testing file operations."""
    return tmp_path

# Fixture for setting up test environment
@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """Sets up the test environment with required directories."""
    # Create necessary directories if they don't exist
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    # Return any context needed for tests
    return {} 