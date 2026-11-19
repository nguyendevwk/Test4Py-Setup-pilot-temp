import pytest
from string_utils.manipulation import reverse
from string_utils.errors import InvalidInputError

def test_reverse_basic():
    """Normal case: reverse a simple ASCII string."""
    original = "hello"
    expected = "olleh"
    assert reverse(original) == expected

def test_reverse_boundary_unicode():
    """Boundary case: reverse a string containing Unicode characters."""
    original = "héllo 🌍"
    expected = "🌍 olléh"
    assert reverse(original) == expected

def test_reverse_invalid_input():
    """Error case: passing a non-string should raise InvalidInputError."""
    with pytest.raises(InvalidInputError):
        reverse(123)  # non-string input
