import decimal
import pytest
from typesystem.fields import Number
from typesystem.base import ValidationError

def test_number_valid_with_constraints():
    field = Number(minimum=0, maximum=10, multiple_of=2, precision="0.01")
    result = field.validate("4.567")
    # value should be rounded to two decimal places and cast to int because numeric_type is None
    assert isinstance(result, int)
    assert result == 5  # 4.567 rounded to 4.57, cast to int gives 4, but int(4.57) -> 4; however rounding to 4.57 then int gives 4
    # Actually int(4.57) is 4, so adjust expectation
    assert result == 4

def test_number_exclusive_minimum_boundary():
    field = Number(exclusive_minimum=5)
    with pytest.raises(ValidationError) as excinfo:
        field.validate(5)
    assert "exclusive_minimum" in str(excinfo.value)

def test_number_multiple_of_error():
    field = Number(multiple_of=3)
    with pytest.raises(ValidationError) as excinfo:
        field.validate(10)
    assert "multiple_of" in str(excinfo.value)
