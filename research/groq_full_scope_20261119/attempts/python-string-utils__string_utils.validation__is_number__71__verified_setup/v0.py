import pytest
from string_utils.validation import is_number
from string_utils.errors import InvalidInputError

def test_is_number_valid_cases():
    # Valid integer, float, signed, and scientific notation
    assert is_number("42") is True
    assert is_number("-9.12") is True
    assert is_number("+3.1415") is True
    assert is_number("1e3") is True
    assert is_number("-2E-5") is True

def test_is_number_invalid_cases():
    # Invalid strings that should return False
    assert is_number("1 2 3") is False
    assert is_number("abc") is False
    assert is_number("1.2.3") is False
    assert is_number("") is False
    assert is_number("   ") is False

def test_is_number_type_error():
    # Non-string input should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        is_number(123)
    with pytest.raises(InvalidInputError):
        is_number(None)
    with pytest.raises(InvalidInputError):
        is_number(["1", "2"])
