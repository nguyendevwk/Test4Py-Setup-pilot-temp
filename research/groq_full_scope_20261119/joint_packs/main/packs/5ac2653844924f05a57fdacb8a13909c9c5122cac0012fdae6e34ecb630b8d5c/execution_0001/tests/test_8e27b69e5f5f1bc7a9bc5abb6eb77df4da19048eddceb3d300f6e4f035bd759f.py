import pytest
from string_utils.manipulation import reverse
from string_utils.errors import InvalidInputError

def test_reverse_basic():
    """Normal case: simple ASCII string."""
    assert reverse("hello") == "olleh"

def test_reverse_unicode_and_empty():
    """Boundary case: empty string and Unicode characters."""
    # Empty string should return empty string
    assert reverse("") == ""
    # Unicode string with combining characters
    original = "café"
    # The reverse should preserve grapheme order
    assert reverse(original) == "éfac"

def test_reverse_invalid_input():
    """Error case: non-string input should raise InvalidInputError."""
    with pytest.raises(InvalidInputError):
        reverse(123)  # integer input
