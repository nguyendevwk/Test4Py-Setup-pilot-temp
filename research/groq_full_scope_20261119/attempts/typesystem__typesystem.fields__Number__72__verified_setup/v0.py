import decimal
import pytest
from typesystem.fields import Number


def test_number_valid_and_precision():
    """Validate a normal number and check precision rounding."""
    field = Number(minimum=0, maximum=10, precision="0.01")
    # Valid integer input
    assert field.validate(5) == 5
    # Valid float input within bounds
    assert field.validate(3.14159) == 3.14
    # String input coerced to decimal and rounded
    assert field.validate("2.71828") == 2.72
    # Value exactly at maximum
    assert field.validate(10) == 10
    # Value just below minimum should raise
    with pytest.raises(Exception) as excinfo:
        field.validate(-0.01)
    assert "minimum" in str(excinfo.value)


def test_number_boundary_exclusive_and_nan():
    """Test exclusive bounds and non‑finite values."""
    field = Number(
        exclusive_minimum=0,
        exclusive_maximum=5,
        coerce_types=True,
    )
    # Value equal to exclusive_minimum should fail
    with pytest.raises(Exception) as excinfo:
        field.validate(0)
    assert "exclusive_minimum" in str(excinfo.value)

    # Value equal to exclusive_maximum should fail
    with pytest.raises(Exception) as excinfo:
        field.validate(5)
    assert "exclusive_maximum" in str(excinfo.value)

    # Non‑finite values are rejected
    for bad in (float("inf"), float("-inf"), float("nan")):
        with pytest.raises(Exception) as excinfo:
            field.validate(bad)
        assert "finite" in str(excinfo.value)


def test_number_multiple_of_and_type_errors():
    """Check multiple_of constraint and type validation."""
    field = Number(multiple_of=3)
    # Valid multiple
    assert field.validate(9) == 9
    # Invalid multiple raises error
    with pytest.raises(Exception) as excinfo:
        field.validate(10)
    assert "multiple_of" in str(excinfo.value)

    # Boolean is not a number
    with pytest.raises(Exception) as excinfo:
        field.validate(True)
    assert "type" in str(excinfo.value)

    # String that cannot be parsed as number
    with pytest.raises(Exception) as excinfo:
        field.validate("not_a_number")
    assert "type" in str(excinfo.value)
