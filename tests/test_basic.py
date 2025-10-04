import sys
import os
sys.path.append('src')
def test_imports():
    from data.data_preprocessing import preprocess_text
    assert callable(preprocess_text)
