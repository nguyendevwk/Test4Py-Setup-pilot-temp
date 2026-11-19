import pytest
from string_utils.validation import is_integer
from string_utils.errors import InvalidInputError

def test_is_integer_with_valid_integer():
    """Normal case: a plain integer string should return True."""
    assert is_integer("123") is True

def test_is_integer_excludes_decimal_and_scientific():
    """Boundary case: strings that look numeric but contain a decimal point or
    scientific notation should be rejected as integers."""
    assert is_integer("42.0") is False
    assert is_integer("1e3") is False

def test_is_integer_raises_on_non_string_input():
    """Error case: passing a non-string should raise InvalidInputError."""
    with pytest.raises(InvalidInputError):
        is_integer(42)
