import decimal
import pytest
from typesystem.fields import Decimal
from typesystem import ValidationError

# Test 1: Serialization of Decimal values
def test_decimal_serialization():
    field = Decimal()
    # None should serialize to None
    assert field.serialize(None) is None
    # Decimal should be converted to float
    dec_value = decimal.Decimal("123.45")
    assert field.serialize(dec_value) == 123.45
    # Integer should be converted to float
    assert field.serialize(10) == 10.0

# Test 2: Validation accepts valid numeric inputs
def test_decimal_validation_valid():
    field = Decimal()
    # Valid Decimal instance
    assert field.validate(decimal.Decimal("1.2345")).value == decimal.Decimal("1.2345")
    # Valid float
    assert field.validate(3.1415).value == decimal.Decimal("3.1415")
    # Valid int
    assert field.validate(42).value == decimal.Decimal("42")

# Test 3: Validation rejects non-numeric inputs
def test_decimal_validation_invalid():
    field = Decimal()
    # String that cannot be converted to Decimal
    with pytest.raises(ValidationError):
        field.validate("not a number")
    # List input
    with pytest.raises(ValidationError):
        field.validate([1, 2, 3])
    # None is allowed? If not, test that it raises
    if field.required:
        with pytest.raises(ValidationError):
            field.validate(None)
