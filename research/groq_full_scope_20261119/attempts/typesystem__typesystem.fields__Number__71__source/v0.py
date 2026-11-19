import decimal
import pytest
from typesystem.fields import Number
from typesystem.base import ValidationError

def test_number_valid_and_precision(tmp_path):
    # Valid integer, float, and string casting with precision rounding
    field = Number(precision="0.01")
    assert field.validate(10) == 10
    assert field.validate(10.123) == 10.12  # rounded down
    assert field.validate("10.129") == 10.13  # rounded up
    # Ensure precision rounding uses the specified numeric type
    field_int = Number(precision="0.1", numeric_type=int)
    assert field_int.validate(10.9) == 11  # rounded to nearest integer

def test_number_boundary_conditions():
    # Minimum and maximum inclusive
    field = Number(minimum=0, maximum=100)
    assert field.validate(0) == 0
    assert field.validate(100) == 100
    # Exclusive boundaries
    field_excl = Number(exclusive_minimum=0, exclusive_maximum=100)
    with pytest.raises(ValidationError):
        field_excl.validate(0)
    with pytest.raises(ValidationError):
        field_excl.validate(100)
    # Multiple of constraint
    field_multi = Number(multiple_of=5)
    assert field_multi.validate(10) == 10
    with pytest.raises(ValidationError):
        field_multi.validate(12)

def test_number_error_cases():
    field = Number()
    # Null not allowed
    with pytest.raises(ValidationError):
        field.validate(None)
    # Boolean is invalid
    with pytest.raises(ValidationError):
        field.validate(True)
    # Non-numeric string without coercion
    field_no_coerce = Number(coerce_types=False)
    with pytest.raises(ValidationError):
        field_no_coerce.validate("123")
    # Non-finite values
    with pytest.raises(ValidationError):
        field.validate(float("nan"))
    with pytest.raises(ValidationError):
        field.validate(float("inf"))
