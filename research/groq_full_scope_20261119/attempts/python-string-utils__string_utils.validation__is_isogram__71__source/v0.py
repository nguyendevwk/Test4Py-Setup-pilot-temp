import pytest
from string_utils.validation import is_isogram

def test_is_isogram_with_valid_isogram():
    # A known isogram: all letters unique
    assert is_isogram("dermatoglyphics") is True

def test_is_isogram_with_non_isogram_and_empty_string():
    # Non-isogram: repeated 'l'
    assert is_isogram("hello") is False
    # Empty string should not be considered an isogram
    assert is_isogram("") is False

def test_is_isogram_with_invalid_input_types():
    # Passing a non-string type should return False, not raise
    assert is_isogram(12345) is False
    assert is_isogram(None) is False
