import pytest
from flutes.iterator import take

def test_take_normal():
    """Take the first 3 elements from a list."""
    result = list(take(3, [10, 20, 30, 40, 50]))
    assert result == [10, 20, 30], "Should return the first three elements"

def test_take_boundary():
    """When n exceeds the iterable length, return all elements without error."""
    data = (x for x in range(5))  # generator
    result = list(take(10, data))
    assert result == [0, 1, 2, 3, 4], "Should return all elements when n is larger than iterable"

def test_take_negative_n():
    """Providing a negative n should raise ValueError."""
    with pytest.raises(ValueError, match="`n` should be non-negative"):
        list(take(-1, [1, 2, 3]))
