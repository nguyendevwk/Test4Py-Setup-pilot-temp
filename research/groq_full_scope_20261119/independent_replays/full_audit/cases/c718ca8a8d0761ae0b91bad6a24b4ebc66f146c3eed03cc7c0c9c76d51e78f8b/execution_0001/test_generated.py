import pytest
from string_utils.manipulation import reverse
from string_utils.errors import InvalidInputError

def test_reverse_basic():
    """Normal case: simple ASCII string."""
    assert reverse("hello") == "olleh"

def test_reverse_boundary_unicode():
    """Boundary case: string with Unicode characters and combining marks."""
    # The string contains a base character followed by a combining acute accent.
    s = "a\u0301bc"  # 'ábc'
    # Reversing should keep the combining mark attached to its base character.
    assert reverse(s) == "cb\u0301a"

def test_reverse_invalid_input():
    """Error case: non-string input should raise InvalidInputError."""
    with pytest.raises(InvalidInputError):
        reverse(123)  # passing an integer instead of a string
