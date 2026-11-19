import pytest
from string_utils.validation import is_decimal, is_number
from string_utils.errors import InvalidInputError

def test_is_decimal_with_valid_decimal_and_integer():
    # Valid decimal string should return True
    assert is_decimal("3.1415") is True
    # Integer string should return False even though is_number would be True
    assert is_decimal("42") is False
    # Scientific notation with decimal point should return True
    assert is_decimal("1.2e3") is True
    # Scientific notation without decimal point should return False
    assert is_decimal("1e3") is False

def test_is_decimal_boundary_cases():
    # Leading and trailing spaces should cause is_number to fail, hence False
    assert is_decimal(" 3.14 ") is False
    # Empty string should be False
    assert is_decimal("") is False
    # String with only a decimal point should be False
    assert is_decimal(".") is False
    # Negative decimal with exponent should be True
    assert is_decimal("-2.5e-4") is True

def test_is_decimal_invalid_input_type():
    # Passing a non-string type should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        is_decimal(42)  # type: ignore[arg-type]
    with pytest.raises(InvalidInputError):
        is_decimal(None)  # type: ignore[arg-type]
