import decimal
import pytest
from typesystem import fields
from typesystem import ValidationError

# Test 1: Normal coercion and serialization
def test_decimal_coercion_and_serialization():
    # Create a Decimal field with default settings
    dec_field = fields.Decimal()
    # Validate an integer (should be coerced to Decimal)
    result = dec_field.validate(42)
    assert result.value == decimal.Decimal("42")
    # Validate a string that represents a decimal
    result = dec_field.validate("3.14")
    assert result.value == decimal.Decimal("3.14")
    # Serialize the Decimal value back to float
    assert dec_field.serialize(result.value) == 3.14

# Test 2: Boundary conditions with minimum and maximum
def test_decimal_min_max_boundary():
    # Minimum inclusive, maximum exclusive
    dec_field = fields.Decimal(minimum=decimal.Decimal("1.0"), maximum=decimal.Decimal("5.0"))
    # Value exactly at minimum should pass
    result = dec_field.validate("1.0")
    assert result.value == decimal.Decimal("1.0")
    # Value just below maximum should pass
    result = dec_field.validate("4.999999")
    assert result.value == decimal.Decimal("4.999999")
    # Value equal to maximum should fail
    with pytest.raises(ValidationError) as excinfo:
        dec_field.validate("5.0")
    assert "maximum" in str(excinfo.value).lower()
    # Value below minimum should fail
    with pytest.raises(ValidationError) as excinfo:
        dec_field.validate("0.999")
    assert "minimum" in str(excinfo.value).lower()

# Test 3: Error handling for invalid input types
def test_decimal_invalid_input():
    dec_field = fields.Decimal()
    # Passing a non-numeric string should raise ValidationError
    with pytest.raises(ValidationError) as excinfo:
        dec_field.validate("not a number")
    assert "invalid" in str(excinfo.value).lower()
    # Passing a complex number should raise ValidationError
    with pytest.raises(ValidationError) as excinfo:
        dec_field.validate(complex(1, 2))
    assert "invalid" in str(excinfo.value).lower()
