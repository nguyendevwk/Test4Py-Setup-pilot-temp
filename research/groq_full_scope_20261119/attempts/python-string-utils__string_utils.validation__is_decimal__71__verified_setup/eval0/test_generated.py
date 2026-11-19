import pytest
from string_utils.validation import is_decimal

def test_is_decimal_with_standard_decimal():
    # Standard decimal string should return True
    assert is_decimal("123.456") is True
    # Integer string without a dot should return False
    assert is_decimal("789") is False

def test_is_decimal_with_scientific_notation():
    # Scientific notation containing a dot should be considered decimal
    assert is_decimal("1.23e10") is True
    # Scientific notation without a dot should be considered integer
    assert is_decimal("1e10") is False

def test_is_decimal_with_invalid_input():
    # Passing a non-string (e.g., None) should raise a TypeError
    with pytest.raises(TypeError):
        is_decimal(None)
