import pytest
from string_utils.validation import is_isogram

def test_is_isogram_true_case():
    """A known isogram should return True."""
    assert is_isogram('dermatoglyphics') is True

def test_is_isogram_boundary_empty_string():
    """An empty string is not a full string, so should return False."""
    assert is_isogram('') is False

def test_is_isogram_non_string_input():
    """Non‑string inputs are treated as not full strings and return False."""
    assert is_isogram(123) is False
