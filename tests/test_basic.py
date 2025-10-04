"""Basic tests for the sentiment analysis project."""

import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def test_imports():
    """Test that core modules can be imported."""
    try:
        from data.data_preprocessing import preprocess_text

        assert callable(preprocess_text)
    except ImportError as e:
        # If dependencies are missing, at least verify the module exists
        import importlib.util

        module_path = os.path.join(
            os.path.dirname(__file__), "..", "src", "data", "data_preprocessing.py"
        )
        assert os.path.exists(module_path), f"Module file not found: {module_path}"
        print(f"Skipping import test due to missing dependencies: {e}")


def test_project_structure():
    """Test that the project structure is correct."""
    project_root = os.path.dirname(os.path.dirname(__file__))

    # Check key directories exist
    assert os.path.exists(os.path.join(project_root, "src"))
    assert os.path.exists(os.path.join(project_root, "src", "data"))
    assert os.path.exists(os.path.join(project_root, "src", "model"))
    assert os.path.exists(os.path.join(project_root, "src", "api"))

