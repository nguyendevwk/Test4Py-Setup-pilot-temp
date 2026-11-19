import pytest
from string_utils.manipulation import reverse
from string_utils.errors import InvalidInputError

def test_reverse_basic():
    """Normal case: simple ASCII string."""
    assert reverse("hello") == "olleh"

def test_reverse_boundary_empty_and_unicode():
    """Boundary cases: empty string and Unicode characters."""
    assert reverse("") == ""
    # Unicode string with combining characters
    original = "café"
    # The reverse should preserve grapheme order, not codepoint order
    assert reverse(original) == "éfac"

def test_reverse_invalid_input_raises_error():
    """Error case: non-string input should raise InvalidInputError."""
    with pytest.raises(InvalidInputError):
        reverse(123)  # integer input
