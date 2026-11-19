import decimal
import pytest
from typesystem import ValidationError
from typesystem.fields import Decimal

# Test 1: Normal validation and serialization of a Decimal value
def test_decimal_normal_value():
    field = Decimal()
    # Validate a Decimal instance
    result = field.validate(decimal.Decimal("12.34"))
    assert result.is_valid
    assert result.value == decimal.Decimal("12.34")
    # Serialize the validated value
    serialized = field.serialize(result.value)
    assert serialized == 12.34  # float conversion
    # Validate a numeric type that can be coerced
    result2 = field.validate(56)
    assert result2.is_valid
    assert result2.value == decimal.Decimal("56")

# Test 2: Boundary checks with minimum and maximum constraints
def test_decimal_boundary_constraints():
    field = Decimal(minimum=decimal.Decimal("0.0"), maximum=decimal.Decimal("10.0"))
    # Value within bounds
    res_in = field.validate(decimal.Decimal("5.5"))
    assert res_in.is_valid
    # Value equal to minimum
    res_min = field.validate(decimal.Decimal("0.0"))
    assert res_min.is_valid
    # Value equal to maximum
    res_max = field.validate(decimal.Decimal("10.0"))
    assert res_max.is_valid
    # Value below minimum
    with pytest.raises(ValidationError) as exc_min:
        field.validate(decimal.Decimal("-1"))
    assert "must be greater than or equal to" in str(exc_min.value)
    # Value above maximum
    with pytest.raises(ValidationError) as exc_max:
        field.validate(decimal.Decimal("11"))
    assert "must be less than or equal to" in str(exc_max.value)

# Test 3: Error handling for invalid input types
def test_decimal_invalid_input():
    field = Decimal()
    # Passing a string that cannot be converted to Decimal
    with pytest.raises(ValidationError) as exc:
        field.validate("not a number")
    assert "is not a valid decimal" in str(exc.value)
    # Passing a complex number (unsupported type)
    with pytest.raises(ValidationError) as exc_complex:
        field.validate(complex(1, 2))
    assert "is not a valid decimal" in str(exc_complex.value)
