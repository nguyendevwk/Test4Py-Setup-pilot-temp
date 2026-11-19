import pytest
from string_utils.validation import is_number
from string_utils.errors import InvalidInputError

def test_is_number_valid_cases():
    # Normal numeric strings
    assert is_number("42") is True
    assert is_number("-9.12") is True
    assert is_number("+3.14") is True
    assert is_number("1e5") is True
    assert is_number("-2E-3") is True
    # Edge cases: leading/trailing spaces should be invalid
    assert is_number(" 42") is False
    assert is_number("42 ") is False
    # Non-numeric content
    assert is_number("1 2 3") is False
    assert is_number("abc") is False

def test_is_number_boundary_and_format():
    # Numbers with no decimal point but with exponent
    assert is_number("0e0") is True
    # Numbers with decimal but no integer part
    assert is_number(".5") is False  # assuming regex requires leading digit
    # Numbers with exponent but no mantissa
    assert is_number("e10") is False
    # Very large number
    assert is_number("9.223372036854776e+18") is True

def test_is_number_invalid_input_type():
    # Passing non-string types should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        is_number(42)
    with pytest.raises(InvalidInputError):
        is_number(None)
    with pytest.raises(InvalidInputError):
        is_number([1, 2, 3])
