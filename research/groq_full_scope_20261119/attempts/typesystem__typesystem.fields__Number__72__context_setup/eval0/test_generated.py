import decimal
import pytest
from typesystem.fields import Number
from typesystem.base import ValidationError

def test_number_coercion_and_precision(tmp_path):
    # Create a Number field that coerces strings to int and rounds to 2 decimal places
    field = Number(coerce_types=True, precision="0.01")
    # Valid integer string should be coerced to int
    assert field.validate("42") == 42
    # Valid float string should be coerced to Decimal then rounded
    assert field.validate("3.14159") == 3.14
    # Valid Decimal input should be rounded
    assert field.validate(decimal.Decimal("2.71828")) == 2.72
    # Empty string with allow_null should return None
    field_null = Number(allow_null=True, coerce_types=True)
    assert field_null.validate("") is None

def test_number_boundary_conditions():
    # Minimum and maximum boundaries
    field = Number(minimum=0, maximum=10)
    assert field.validate(0) == 0
    assert field.validate(10) == 10
    # Exclusive boundaries
    field_excl = Number(exclusive_minimum=0, exclusive_maximum=10)
    assert field_excl.validate(1) == 1
    assert field_excl.validate(9) == 9
    # Multiple of constraint
    field_multi = Number(multiple_of=5)
    assert field_multi.validate(15) == 15
    # Multiple of with float
    field_multi_float = Number(multiple_of=0.5)
    assert field_multi_float.validate(1.5) == 1.5

def test_number_error_messages():
    field = Number(minimum=5, maximum=10, multiple_of=2)
    # Below minimum
    with pytest.raises(ValidationError) as excinfo:
        field.validate(4)
    assert "minimum" in excinfo.value.text
    # Above maximum
    with pytest.raises(ValidationError) as excinfo:
        field.validate(11)
    assert "maximum" in excinfo.value.text
    # Not a multiple of 2
    with pytest.raises(ValidationError) as excinfo:
        field.validate(7)
    assert "multiple_of" in excinfo.value.text
    # Non-numeric type
    with pytest.raises(ValidationError) as excinfo:
        field.validate("not a number")
    assert "type" in excinfo.value.text
