import pytest
from string_utils.manipulation import reverse
from string_utils.errors import InvalidInputError

def test_reverse_normal():
    """Normal case: reverse a typical string."""
    original = "OpenAI"
    expected = "IAnepO"
    result = reverse(original)
    assert result == expected
    assert result != original  # ensure it is actually reversed

def test_reverse_boundary_empty_and_single():
    """Boundary cases: empty string and single character."""
    # Empty string
    assert reverse("") == ""
    # Single character
    assert reverse("x") == "x"

def test_reverse_invalid_input():
    """Error case: non-string input should raise InvalidInputError."""
    with pytest.raises(InvalidInputError):
        reverse(123)          # integer
    with pytest.raises(InvalidInputError):
        reverse(None)         # NoneType
    with pytest.raises(InvalidInputError):
        reverse(['a', 'b'])   # list
