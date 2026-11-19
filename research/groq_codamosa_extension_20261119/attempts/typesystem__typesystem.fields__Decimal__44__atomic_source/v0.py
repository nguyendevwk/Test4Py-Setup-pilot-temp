import decimal
import pytest
from typesystem.fields import Decimal
from typesystem import ValidationError

def test_decimal_serialize_none_and_float():
    """Decimal.serialize should return None for None and float for Decimal values."""
    field = Decimal()
    assert field.serialize(None) is None
    d = decimal.Decimal("123.456")
    # The serialize method converts to float
    assert field.serialize(d) == 123.456

def test_decimal_validation_accepts_decimal_and_int_float():
    """Decimal.validate should accept Decimal, int, and float values."""
    field = Decimal()
    # Valid Decimal
    assert field.validate(decimal.Decimal("10.5")) == decimal.Decimal("10.5")
    # Valid int
    assert field.validate(42) == decimal.Decimal("42")
    # Valid float
    assert field.validate(3.14) == decimal.Decimal("3.14")

def test_decimal_validation_rejects_invalid_types_and_nan():
    """Decimal.validate should raise ValidationError for non-numeric types and NaN."""
    field = Decimal()
    # Non-numeric type
    with pytest.raises(ValidationError):
        field.validate("not a number")
    # NaN value
    with pytest.raises(ValidationError):
        field.validate(decimal.Decimal("NaN"))
