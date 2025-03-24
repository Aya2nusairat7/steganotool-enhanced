import os
import sys
import pytest

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# pytest configuration
def pytest_configure(config):
    """Configure pytest."""
    # Add markers or other configuration here if needed
    pass

@pytest.fixture(scope='function')
def temp_output_dir(tmpdir):
    """Create a temporary directory for test outputs."""
    output_dir = tmpdir.mkdir("output")
    return str(output_dir)

@pytest.fixture(scope='function')
def temp_upload_dir(tmpdir):
    """Create a temporary directory for test uploads."""
    upload_dir = tmpdir.mkdir("uploads")
    return str(upload_dir) 