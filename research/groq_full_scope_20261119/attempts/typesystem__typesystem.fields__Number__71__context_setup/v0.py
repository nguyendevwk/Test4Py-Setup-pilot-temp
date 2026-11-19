import decimal
import pytest
from typesystem.fields import Number
from typesystem.base import ValidationError

def test_number_coerce_and_precision(tmp_path):
    # Create a Number field that coerces strings to int and rounds to 2 decimal places
    field = Number(
        numeric_type=int,
        precision="0.01",
        coerce_types=True,
    )
    # Valid integer string should be coerced to int
    assert field.validate("42") == 42
    # Valid float string should be coerced to int (truncated)
    assert field.validate("42.7") == 42
    # Value with more precision should be rounded before conversion
    assert field.validate("42.123") == 42
    # Negative number with precision
    assert field.validate("-1.234") == -1

def test_number_boundary_and_multiple_of():
    # Field with minimum, maximum, exclusive bounds and multiple_of
    field = Number(
        minimum=0,
        maximum=10,
        exclusive_minimum=0,
        exclusive_maximum=10,
        multiple_of=2,
        coerce_types=True,
    )
    # 2 is valid (>= exclusive_minimum and <= exclusive_maximum)
    assert field.validate(2) == 2
    # 10 is invalid because it equals exclusive_maximum
    with pytest.raises(ValidationError) as excinfo:
        field.validate(10)
    assert "exclusive_maximum" in excinfo.value.text
    # 1 is invalid because not a multiple of 2
    with pytest.raises(ValidationError) as excinfo:
        field.validate(1)
    assert "multiple_of" in excinfo.value.text

def test_number_error_cases():
    # Field that does not allow null and does not coerce types
    field = Number(
        coerce_types=False,
        allow_null=False,
    )
    # None should raise null error
    with pytest.raises(ValidationError) as excinfo:
        field.validate(None)
    assert "null" in excinfo.value.text
    # Boolean should raise type error
    with pytest.raises(ValidationError) as excinfo:
        field.validate(True)
    assert "type" in excinfo.value.text
    # String that cannot be parsed to number should raise type error
    with pytest.raises(ValidationError) as excinfo:
        field.validate("not a number")
    assert "type" in excinfo.value.text
