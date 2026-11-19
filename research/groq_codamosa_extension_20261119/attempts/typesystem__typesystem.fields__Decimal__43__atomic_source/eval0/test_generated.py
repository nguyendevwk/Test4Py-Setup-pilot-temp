import decimal
import pytest
from typesystem.fields import Decimal
from typesystem import ValidationError

def test_decimal_valid_input():
    field = Decimal()
    # Valid decimal string
    result = field.validate("123.45")
    assert isinstance(result, decimal.Decimal)
    assert result == decimal.Decimal("123.45")
    # Valid numeric input
    result = field.validate(678)
    assert isinstance(result, decimal.Decimal)
    assert result == decimal.Decimal("678")
    # None input returns None
    assert field.validate(None) is None

def test_decimal_boundary_large_value():
    field = Decimal()
    # Very large decimal value
    large_str = "9" * 1000 + ".123456789"
    result = field.validate(large_str)
    assert isinstance(result, decimal.Decimal)
    assert str(result) == large_str

def test_decimal_invalid_input_raises():
    field = Decimal()
    # Invalid string should raise ValidationError
    with pytest.raises(ValidationError):
        field.validate("not a number")
    # Invalid type (list) should raise ValidationError
    with pytest.raises(ValidationError):
        field.validate([1, 2, 3])
