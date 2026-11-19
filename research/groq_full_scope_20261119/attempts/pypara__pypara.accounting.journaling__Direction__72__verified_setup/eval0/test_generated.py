import pytest
from pypara.accounting.journaling import Direction
from pypara.commons.numbers import Quantity


def test_direction_of_positive_quantity():
    """Direction.of should return INC for a positive quantity."""
    pos = Quantity(10)
    assert Direction.of(pos) is Direction.INC


def test_direction_of_negative_quantity():
    """Direction.of should return DEC for a negative quantity."""
    neg = Quantity(-7)
    assert Direction.of(neg) is Direction.DEC


def test_direction_of_zero_quantity_raises():
    """Direction.of should raise AssertionError when quantity is zero."""
    zero = Quantity(0)
    with pytest.raises(AssertionError) as excinfo:
        Direction.of(zero)
    assert "0 quantity" in str(excinfo.value)
