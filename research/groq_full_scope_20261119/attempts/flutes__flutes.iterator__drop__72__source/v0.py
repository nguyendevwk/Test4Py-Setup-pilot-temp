import pytest
from flutes.iterator import drop

def test_drop_normal():
    """Dropping a positive number of elements from a finite iterable."""
    data = [10, 20, 30, 40, 50]
    result = list(drop(2, data))
    assert result == [30, 40, 50], "Should drop the first two elements"

def test_drop_boundary():
    """Dropping more elements than the iterable contains should yield an empty iterator."""
    data = [1, 2]
    result = list(drop(5, data))
    assert result == [], "Dropping more than length should return empty iterator"

def test_drop_negative_raises():
    """Providing a negative n should raise ValueError."""
    with pytest.raises(ValueError, match="`n` should be non-negative"):
        list(drop(-1, [1, 2, 3]))
