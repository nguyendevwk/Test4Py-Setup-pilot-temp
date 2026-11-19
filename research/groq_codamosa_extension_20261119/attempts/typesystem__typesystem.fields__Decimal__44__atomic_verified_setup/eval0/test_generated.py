import decimal
import pytest
from typesystem import fields
from typesystem.exceptions import ValidationError

# Test 1: Normal serialization and validation within bounds
def test_decimal_normal_behavior():
    # Create a Decimal field with a precision and bounds
    field = fields.Decimal(minimum=decimal.Decimal("1.5"),
                           maximum=decimal.Decimal("10.5"),
                           precision="2",
                           coerce_types=True)
    # Valid value within bounds
    value = decimal.Decimal("5.1234")
    # Validation should succeed
    result = field.validate(value)
    assert result.is_valid
    # The validated value should be coerced to Decimal with correct precision
    assert isinstance(result.value, decimal.Decimal)
    assert result.value == decimal.Decimal("5.12")  # rounded to 2 decimal places
    # Serialization should return a float
    assert field.serialize(result.value) == 5.12

# Test 2: Boundary condition with exclusive minimum
def test_decimal_exclusive_minimum():
    field = fields.Decimal(minimum=decimal.Decimal("0"),
                           exclusive_minimum=decimal.Decimal("0"),
                           coerce_types=True)
    # Value equal to exclusive minimum should fail
    with pytest.raises(ValidationError) as excinfo:
        field.validate(decimal.Decimal("0"))
    assert "exclusive minimum" in str(excinfo.value).lower()
    # Value just above exclusive minimum should pass
    result = field.validate(decimal.Decimal("0.0001"))
    assert result.is_valid
    assert result.value == decimal.Decimal("0.0001")

# Test 3: Error on invalid type when coerce_types is False
def test_decimal_invalid_type_no_coerce():
    field = fields.Decimal(coerce_types=False)
    # Passing a string should raise ValidationError
    with pytest.raises(ValidationError) as excinfo:
        field.validate("not a number")
    assert "expected a number" in str(excinfo.value).lower()
    # Passing a float should also raise ValidationError
    with pytest.raises(ValidationError) as excinfo:
        field.validate(3.14)
    assert "expected a number" in str(excinfo.value).lower()
