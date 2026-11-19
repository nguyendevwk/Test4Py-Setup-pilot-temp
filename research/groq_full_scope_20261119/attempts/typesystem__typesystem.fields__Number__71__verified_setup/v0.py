import decimal
import pytest
from typesystem.fields import Number
from typesystem.base import ValidationError

def test_number_valid_and_precision():
    # Normal numeric validation with precision rounding
    field = Number(minimum=0, maximum=10, precision="0.01")
    result = field.validate("3.14159")
    assert isinstance(result, float)
    assert result == 3.14  # rounded to two decimal places

    # Integer enforcement when numeric_type is int
    field_int = Number(numeric_type=int, minimum=1, maximum=5)
    assert field_int.validate(3) == 3
    with pytest.raises(ValidationError) as excinfo:
        field_int.validate(3.5)  # float not integer
    assert "integer" in str(excinfo.value)

def test_number_boundary_conditions():
    # Inclusive minimum and maximum
    field = Number(minimum=0, maximum=5)
    assert field.validate(0) == 0
    assert field.validate(5) == 5

    # Exclusive boundaries
    field_excl = Number(exclusive_minimum=0, exclusive_maximum=5)
    with pytest.raises(ValidationError) as excinfo:
        field_excl.validate(0)
    assert "exclusive_minimum" in str(excinfo.value)
    with pytest.raises(ValidationError) as excinfo:
        field_excl.validate(5)
    assert "exclusive_maximum" in str(excinfo.value)

    # Multiple of constraint
    field_multi = Number(multiple_of=0.5)
    assert field_multi.validate(1.0) == 1.0
    with pytest.raises(ValidationError) as excinfo:
        field_multi.validate(1.3)
    assert "multiple_of" in str(excinfo.value)

def test_number_error_cases():
    field = Number(minimum=10, coerce_types=False)
    # Null not allowed
    with pytest.raises(ValidationError) as excinfo:
        field.validate(None)
    assert "null" in str(excinfo.value)

    # Non-numeric string when coercion disabled
    with pytest.raises(ValidationError) as excinfo:
        field.validate("abc")
    assert "type" in str(excinfo.value)

    # Infinite value
    with pytest.raises(ValidationError) as excinfo:
        field.validate(float("inf"))
    assert "finite" in str(excinfo.value)

    # Value below minimum
    with pytest.raises(ValidationError) as excinfo:
        field.validate(5)
    assert "minimum" in str(excinfo.value)
