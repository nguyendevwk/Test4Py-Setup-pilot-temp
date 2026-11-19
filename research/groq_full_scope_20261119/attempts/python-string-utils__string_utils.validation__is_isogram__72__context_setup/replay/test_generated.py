import pytest
from string_utils.validation import is_isogram

def test_is_isogram_true():
    """A known isogram should return True."""
    assert is_isogram("dermatoglyphics") is True

def test_is_isogram_false_due_to_repetition():
    """A string with repeated letters should return False."""
    assert is_isogram("hello") is False

def test_is_isogram_invalid_input():
    """Non‑string or empty input should return False."""
    assert is_isogram("") is False
    assert is_isogram("   ") is False
    assert is_isogram(123) is False
