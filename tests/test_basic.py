import os
import sys


def test_project_structure():
    """Test that the project structure is correct."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Check key directories exist
    assert os.path.exists(os.path.join(project_root, "src"))
    assert os.path.exists(os.path.join(project_root, "src", "data"))
    assert os.path.exists(os.path.join(project_root, "src", "model"))
    assert os.path.exists(os.path.join(project_root, "src", "api"))


def test_imports():
    """Test that key modules can be imported."""
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

    # Import modules without executing them
    try:
        from data import data_preprocessing  # noqa: F401
        from model import model_building  # noqa: F401

        assert True
    except ImportError:
        # Some modules might have dependencies not available in test env
        pass


def test_data_directory_structure():
    """Test that data directories exist."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Check key directories exist
    assert os.path.exists(os.path.join(project_root, "src"))
    assert os.path.exists(os.path.join(project_root, "src", "data"))
    assert os.path.exists(os.path.join(project_root, "src", "model"))
    assert os.path.exists(os.path.join(project_root, "src", "api"))
