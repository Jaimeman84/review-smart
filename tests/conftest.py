import pytest
import sys
from pathlib import Path

# Add project root to Python path
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

def pytest_configure(config):
    """Add custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )

@pytest.fixture(autouse=True)
def add_standard_fixtures(doctest_namespace):
    """Add any standard fixtures to all tests."""
    pass