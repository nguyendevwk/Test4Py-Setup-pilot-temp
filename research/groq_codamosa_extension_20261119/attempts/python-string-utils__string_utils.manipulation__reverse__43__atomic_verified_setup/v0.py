import pytest
from string_utils.manipulation import reverse
from string_utils.errors import InvalidInputError

def test_reverse_basic():
    """Normal case: simple ASCII string."""
    original = "hello"
    expected = "olleh"
    assert reverse(original) == expected

def test_reverse_boundary_unicode():
    """Boundary case: string with Unicode characters and emojis."""
    original = "𝔘𝔫𝔦𝔠𝔬𝔡𝔢🚀"
    expected = "🚀𝔢𝔬𝔠𝔦𝔫𝔘"
    assert reverse(original) == expected

def test_reverse_invalid_input():
    """Error case: non-string input should raise InvalidInputError."""
    with pytest.raises(InvalidInputError):
        reverse(123)  # passing an integer instead of a string
