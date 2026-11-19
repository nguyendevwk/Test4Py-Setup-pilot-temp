import pytest
from string_utils.validation import is_decimal

def test_is_decimal_with_standard_decimal():
    # Standard decimal with a fractional part should return True
    assert is_decimal("123.456") is True

def test_is_decimal_with_scientific_notation():
    # Scientific notation containing a decimal point should return True
    assert is_decimal("1.23e4") is True

def test_is_decimal_with_invalid_input_raises_type_error():
    # Passing a non-string should raise a TypeError because is_number expects a string
    with pytest.raises(TypeError):
        is_decimal(42)  # type: ignore[arg-type]
