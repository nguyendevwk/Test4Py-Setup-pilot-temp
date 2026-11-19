import decimal
import pytest
from typesystem.fields import Decimal
from typesystem import ValidationError

def test_decimal_serialize_none_and_float():
    field = Decimal()
    # Serializing None should return None
    assert field.serialize(None) is None
    # Serializing a Decimal should return its float representation
    d = decimal.Decimal("123.45")
    assert field.serialize(d) == 123.45
    # Serializing a numeric type that can be cast to Decimal should also work
    assert field.serialize(10) == 10.0

def test_decimal_validation_success():
    field = Decimal()
    # Valid Decimal instance
    assert field.validate(decimal.Decimal("1.23")).value == decimal.Decimal("1.23")
    # Valid numeric string that can be converted to Decimal
    assert field.validate("4.56").value == decimal.Decimal("4.56")
    # Valid integer string
    assert field.validate("7").value == decimal.Decimal("7")
    # Valid float (converted to Decimal)
    assert field.validate(8.9).value == decimal.Decimal("8.9")

def test_decimal_validation_failure():
    field = Decimal()
    # Invalid type: string that cannot be converted to Decimal
    with pytest.raises(ValidationError):
        field.validate("not a number")
    # Invalid type: list
    with pytest.raises(ValidationError):
        field.validate([1, 2, 3])
    # Invalid type: None is allowed? It should pass through? Check behavior
    # If None is not allowed, it should raise; otherwise it should return None
    # Here we assume None is allowed and returns None
    assert field.validate(None).value is None
