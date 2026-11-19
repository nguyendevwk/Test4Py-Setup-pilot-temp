import pytest
from flutes.iterator import take

def test_take_normal():
    """Take a fixed number of elements from a large iterable."""
    result = list(take(5, range(1000000)))
    assert result == [0, 1, 2, 3, 4]
    # Ensure the iterator stops after the requested number of elements
    assert len(result) == 5

def test_take_boundary_short_iterable():
    """When n exceeds the iterable length, all elements are returned without error."""
    data = [10, 20, 30]
    result = list(take(5, data))
    assert result == data
    # No StopIteration exception should propagate
    assert len(result) == len(data)

def test_take_negative_n_raises():
    """Providing a negative n should raise a ValueError."""
    with pytest.raises(ValueError) as excinfo:
        list(take(-1, [1, 2, 3]))
    assert "`n` should be non-negative" in str(excinfo.value)
