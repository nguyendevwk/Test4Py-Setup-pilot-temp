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
    reversed_str = reverse(original)
    assert reversed_str == "éfac"
    # Ensure reversing twice yields original
    assert reverse(reversed_str) == original

def test_reverse_invalid_input():
    """Error case: non-string input raises InvalidInputError."""
    with pytest.raises(InvalidInputError):
        reverse(123)  # integer input
    with pytest.raises(InvalidInputError):
        reverse(None)  # None input
