import sys
import os
sys.path.append('src')

def test_imports():
    from data.data_preprocessing import preprocess_comment
    assert callable(preprocess_comment)
