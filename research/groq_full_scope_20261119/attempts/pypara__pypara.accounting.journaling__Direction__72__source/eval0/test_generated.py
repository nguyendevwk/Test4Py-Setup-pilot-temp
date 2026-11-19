import pytest
from pypara.accounting.journaling import Direction
from pypara.commons.numbers import Quantity

def test_direction_of_positive_quantity():
    """Direction.of should return INC for a positive quantity."""
    q = Quantity(10)
    assert Direction.of(q) is Direction.INC

def test_direction_of_negative_quantity():
    """Direction.of should return DEC for a negative quantity."""
    q = Quantity(-5)
    assert Direction.of(q) is Direction.DEC

def test_direction_of_zero_quantity_raises():
    """Direction.of should raise an AssertionError when quantity is zero."""
    q = Quantity(0)
    with pytest.raises(AssertionError) as excinfo:
        Direction.of(q)
    assert "0 quantity" in str(excinfo.value)
