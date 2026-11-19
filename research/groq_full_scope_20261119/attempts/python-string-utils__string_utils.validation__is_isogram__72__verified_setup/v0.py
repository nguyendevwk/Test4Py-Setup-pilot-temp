import pytest
from string_utils.validation import is_isogram

def test_isogram_true():
    """A known isogram should return True."""
    assert is_isogram("dermatoglyphics") is True

def test_isogram_false():
    """A string with repeated letters should return False."""
    assert is_isogram("hello") is False

def test_non_string_and_empty():
    """Non‑string input and empty string should both return False."""
    assert is_isogram(123) is False
    assert is_isogram("") is False
