import pytest
from string_utils.validation import is_string

def test_is_string_with_regular_string():
    """Normal case: a non‑empty string should return True."""
    assert is_string("hello") is True

def test_is_string_with_empty_string_and_non_string():
    """Boundary case: empty string is still a string; non‑string returns False."""
    assert is_string("") is True
    assert is_string(123) is False

def test_is_string_with_none_and_bytes():
    """Error‑like inputs: None and bytes should not be considered strings."""
    assert is_string(None) is False
    assert is_string(b"bytes") is False
