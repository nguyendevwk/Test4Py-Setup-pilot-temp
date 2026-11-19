import decimal
import pytest
from typesystem import Decimal, ValidationError

# Test 1: Normal validation with default bounds and coercion
def test_decimal_default_validation():
    field = Decimal()
    # Valid decimal input
    result = field.validate(decimal.Decimal("12.34"))
    assert result.value == decimal.Decimal("12.34")
    # Valid string input should be coerced to Decimal
    result = field.validate("56.78")
    assert result.value == decimal.Decimal("56.78")
    # None should be allowed and return None
    result = field.validate(None)
    assert result.value is None

# Test 2: Boundary checks with inclusive and exclusive limits
def test_decimal_boundary_conditions():
    field = Decimal(minimum=decimal.Decimal("10"), maximum=decimal.Decimal("20"),
                    exclusive_minimum=decimal.Decimal("15"), exclusive_maximum=decimal.Decimal("18"))
    # Value equal to minimum is allowed
    assert field.validate(decimal.Decimal("10")).value == decimal.Decimal("10")
    # Value equal to maximum is allowed
    assert field.validate(decimal.Decimal("20")).value == decimal.Decimal("20")
    # Value equal to exclusive_minimum is rejected
    with pytest.raises(ValidationError):
        field.validate(decimal.Decimal("15"))
    # Value equal to exclusive_maximum is rejected
    with pytest.raises(ValidationError):
        field.validate(decimal.Decimal("18"))
    # Value within exclusive bounds passes
    assert field.validate(decimal.Decimal("16")).value == decimal.Decimal("16")

# Test 3: Error handling for invalid types and precision
def test_decimal_invalid_input_and_precision():
    field = Decimal(precision="2")
    # Invalid type (int) should be coerced to Decimal and then rounded to 2 decimal places
    result = field.validate(123)
    assert result.value == decimal.Decimal("123.00")
    # Invalid string that cannot be converted should raise ValidationError
    with pytest.raises(ValidationError):
        field.validate("not a number")
    # Value exceeding precision should be rounded correctly
    result = field.validate(decimal.Decimal("1.2345"))
    assert result.value == decimal.Decimal("1.23")
