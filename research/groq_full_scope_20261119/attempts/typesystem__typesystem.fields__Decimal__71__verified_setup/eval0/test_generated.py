import decimal
import pytest
from typesystem.fields import Decimal
from typesystem import ValidationError

# Test 1: Normal serialization of a Decimal instance
def test_decimal_serialize_normal():
    field = Decimal()
    value = decimal.Decimal("123.45")
    # serialize should return a float representation
    assert field.serialize(value) == 123.45
    # None should serialize to None
    assert field.serialize(None) is None

# Test 2: Boundary validation with minimum and maximum
def test_decimal_boundary_validation():
    field = Decimal(minimum=decimal.Decimal("10"), maximum=decimal.Decimal("20"))
    # Value within bounds should pass
    result = field.validate(decimal.Decimal("15"))
    assert result.is_valid
    assert result.value == decimal.Decimal("15")
    # Value below minimum should fail
    result = field.validate(decimal.Decimal("5"))
    assert not result.is_valid
    assert "minimum" in result.errors[0].message
    # Value above maximum should fail
    result = field.validate(decimal.Decimal("25"))
    assert not result.is_valid
    assert "maximum" in result.errors[0].message

# Test 3: Validation error for non-numeric input
def test_decimal_invalid_type():
    field = Decimal()
    with pytest.raises(ValidationError) as excinfo:
        field.validate("not a number")
    # The error message should mention the expected type
    assert "Decimal" in str(excinfo.value)
