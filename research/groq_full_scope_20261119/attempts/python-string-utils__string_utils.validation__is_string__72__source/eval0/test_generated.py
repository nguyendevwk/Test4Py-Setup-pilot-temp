import pytest
from string_utils.validation import is_string

def test_is_string_with_regular_string(tmp_path):
    """Normal case: a non‑empty string should return True."""
    assert is_string("hello") is True

def test_is_string_with_empty_string(tmp_path):
    """Boundary case: an empty string should still be considered a string."""
    assert is_string("") is True

def test_is_string_with_non_string_objects(tmp_path):
    """Error case: non‑string objects should return False."""
    assert is_string(123) is False
    assert is_string(b"bytes") is False
    assert is_string(None) is False
    assert is_string([1, 2, 3]) is False
