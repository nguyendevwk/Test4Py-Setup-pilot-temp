import pytest
from string_utils.validation import is_full_string

def test_is_full_string_normal():
    """Normal case: non‑empty string with characters."""
    assert is_full_string("hello") is True

def test_is_full_string_boundary():
    """Boundary case: string with only whitespace should be False."""
    assert is_full_string("   ") is False

def test_is_full_string_error():
    """Error case: non‑string input should return False."""
    assert is_full_string(123) is False
