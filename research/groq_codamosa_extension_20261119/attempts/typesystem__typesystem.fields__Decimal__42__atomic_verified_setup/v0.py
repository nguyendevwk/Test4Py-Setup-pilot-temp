import decimal
import pytest
from typesystem.fields import Decimal
from typesystem import ValidationError

# Test 1: Normal validation and serialization
def test_decimal_normal_and_serialize():
    # Create a Decimal field with a precision and bounds
    field = Decimal(minimum=decimal.Decimal("1.5"), maximum=decimal.Decimal("10.5"), precision="2")
    # Valid value within bounds
    value = decimal.Decimal("5.123")
    result = field.validate(value)
    assert result.is_valid
    # The validated value should be a Decimal instance
    assert isinstance(result.value, decimal.Decimal)
    # Serialization should convert to float
    serialized = field.serialize(result.value)
    assert serialized == 5.123

# Test 2: Boundary check with exclusive minimum
def test_decimal_exclusive_minimum():
    field = Decimal(exclusive_minimum=decimal.Decimal("0"))
    # Value equal to exclusive minimum should fail
    with pytest.raises(ValidationError) as excinfo:
        field.validate(decimal.Decimal("0"))
    assert "exclusive minimum" in str(excinfo.value).lower()
    # Value just above exclusive minimum should pass
    result = field.validate(decimal.Decimal("0.0001"))
    assert result.is_valid
    assert result.value == decimal.Decimal("0.0001")

# Test 3: Error on invalid type
def test_decimal_invalid_type():
    field = Decimal()
    # Passing a string should raise ValidationError
    with pytest.raises(ValidationError) as excinfo:
        field.validate("not a number")
    assert "invalid type" in str(excinfo.value).lower()
