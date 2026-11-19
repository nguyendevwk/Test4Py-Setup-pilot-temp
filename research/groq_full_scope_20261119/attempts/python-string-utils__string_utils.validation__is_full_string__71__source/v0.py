import pytest
from string_utils.validation import is_full_string

def test_is_full_string_with_valid_nonempty_string():
    """Normal case: a non‑empty string with visible characters should return True."""
    assert is_full_string("hello") is True
    assert is_full_string("  hello  ") is True  # leading/trailing spaces are ignored

def test_is_full_string_with_empty_or_whitespace_only():
    """Boundary cases: None, empty string, or only whitespace should return False."""
    assert is_full_string(None) is False
    assert is_full_string("") is False
    assert is_full_string("   ") is False

def test_is_full_string_with_non_string_input():
    """Error scenario: non‑string inputs should be treated as invalid and return False."""
    assert is_full_string(123) is False
    assert is_full_string([1, 2, 3]) is False
    assert is_full_string({"key": "value"}) is False
