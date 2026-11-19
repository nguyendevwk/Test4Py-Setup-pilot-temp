import pytest
from flutes.iterator import take

def test_take_normal():
    """Take a fixed number of elements from a finite iterable."""
    result = list(take(3, [10, 20, 30, 40, 50]))
    assert result == [10, 20, 30], "Should return the first three elements"

def test_take_boundary():
    """When n exceeds the iterable length, all elements are returned without error."""
    data = range(5)
    result = list(take(10, data))
    assert result == [0, 1, 2, 3, 4], "Should return all elements when n is too large"

def test_take_negative_n():
    """Providing a negative n should raise ValueError."""
    with pytest.raises(ValueError) as excinfo:
        list(take(-1, [1, 2, 3]))
    assert "`n` should be non-negative" in str(excinfo.value), "Error message should indicate non-negative requirement"
