import pytest
from pypara.accounting.journaling import Direction
from pypara.commons.numbers import Quantity


def test_direction_of_positive_quantity():
    """Positive quantity should return Direction.INC."""
    qty = Quantity(10)
    assert Direction.of(qty) is Direction.INC
    # Ensure the enum value matches the expected integer
    assert Direction.of(qty).value == 1


def test_direction_of_negative_quantity():
    """Negative quantity should return Direction.DEC."""
    qty = Quantity(-5)
    assert Direction.of(qty) is Direction.DEC
    # Ensure the enum value matches the expected integer
    assert Direction.of(qty).value == -1


def test_direction_of_zero_quantity_raises():
    """Zero quantity should raise an AssertionError."""
    qty = Quantity(0)
    with pytest.raises(AssertionError) as excinfo:
        Direction.of(qty)
    assert "0 quantity" in str(excinfo.value)
