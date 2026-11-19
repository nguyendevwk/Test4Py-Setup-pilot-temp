import pytest
from string_utils.validation import is_isogram
from string_utils.errors import InvalidInputError

def test_is_isogram_true():
    """A known isogram should return True."""
    assert is_isogram("dermatoglyphics") is True

def test_is_isogram_false():
    """A string with repeated letters should return False."""
    assert is_isogram("hello") is False

def test_is_isogram_invalid_input():
    """Non‑string input should raise InvalidInputError."""
    with pytest.raises(InvalidInputError):
        is_isogram(12345)
