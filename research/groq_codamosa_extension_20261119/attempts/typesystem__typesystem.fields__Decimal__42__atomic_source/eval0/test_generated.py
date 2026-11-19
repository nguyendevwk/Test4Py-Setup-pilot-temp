import decimal
import pytest
from typesystem.fields import Decimal
from typesystem.base import ValidationResult, ValidationError

def test_decimal_valid_input_and_serialization():
    field = Decimal()
    # Valid decimal string
    result = field.validate("123.45")
    assert isinstance(result, ValidationResult)
    assert result.is_valid
    assert result.value == decimal.Decimal("123.45")
    # Serialization of a Decimal instance
    serialized = field.serialize(result.value)
    assert serialized == 123.45
    # Serialization of None
    assert field.serialize(None) is None

def test_decimal_boundary_large_value():
    field = Decimal()
    # Very large decimal that is not finite
    large_value = decimal.Decimal("1e1000")
    result = field.validate(large_value)
    assert isinstance(result, ValidationResult)
    assert not result.is_valid
    assert isinstance(result.error, ValidationError)
    # The error message should mention the value is not finite
    assert "finite" in str(result.error)

def test_decimal_invalid_input_raises_error():
    field = Decimal()
    # Invalid string that cannot be converted to Decimal
    with pytest.raises(ValidationError) as excinfo:
        field.validate("not_a_number")
    # The exception message should reference the invalid input
    assert "not_a_number" in str(excinfo.value)
