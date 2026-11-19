import decimal
import pytest
from typesystem.fields import Decimal
from typesystem import ValidationError

def test_decimal_serialize_none_and_float(tmp_path):
    """Decimal.serialize should return None for None and float for Decimal values."""
    field = Decimal()
    # None input
    assert field.serialize(None) is None
    # Decimal input
    d = decimal.Decimal("123.456")
    assert field.serialize(d) == 123.456
    # Ensure the result is a float
    assert isinstance(field.serialize(d), float)

def test_decimal_serialize_invalid_type_raises(tmp_path):
    """Passing a non-numeric type to Decimal.serialize should raise ValidationError."""
    field = Decimal()
    with pytest.raises(ValidationError):
        field.serialize("not a number")

def test_decimal_validation_accepts_numeric_and_rejects_invalid(tmp_path):
    """Decimal.validate should accept numeric types and reject invalid ones."""
    field = Decimal()
    # Accept integer
    assert field.validate(42) == 42
    # Accept float
    assert field.validate(3.14) == 3.14
    # Accept Decimal
    assert field.validate(decimal.Decimal("2.718")) == decimal.Decimal("2.718")
    # Reject string
    with pytest.raises(ValidationError):
        field.validate("invalid")
    # Reject complex number
    with pytest.raises(ValidationError):
        field.validate(1 + 2j)
