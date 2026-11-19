import pytest
from string_utils.manipulation import reverse
from string_utils.errors import InvalidInputError

def test_reverse_normal():
    """Normal case: reverse a typical string."""
    original = "OpenAI"
    expected = "IAnepO"
    result = reverse(original)
    assert result == expected
    # Ensure original string is unchanged
    assert original == "OpenAI"

def test_reverse_boundary_empty_and_single():
    """Boundary cases: empty string and single character."""
    # Empty string
    assert reverse("") == ""
    # Single character
    assert reverse("x") == "x"

def test_reverse_error_non_string():
    """Error case: passing a non-string raises InvalidInputError."""
    with pytest.raises(InvalidInputError):
        reverse(123)  # integer input
    with pytest.raises(InvalidInputError):
        reverse(None)  # None input
