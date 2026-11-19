import pytest
from string_utils.manipulation import reverse
from string_utils.errors import InvalidInputError

def test_reverse_normal():
    """Normal case: reverse a typical string."""
    original = "hello"
    expected = "olleh"
    result = reverse(original)
    assert result == expected
    assert isinstance(result, str)

def test_reverse_boundary_empty():
    """Boundary case: reversing an empty string should return an empty string."""
    original = ""
    expected = ""
    result = reverse(original)
    assert result == expected
    assert result == ""

def test_reverse_error_non_string():
    """Error case: passing a non-string should raise InvalidInputError."""
    with pytest.raises(InvalidInputError):
        reverse(123)
