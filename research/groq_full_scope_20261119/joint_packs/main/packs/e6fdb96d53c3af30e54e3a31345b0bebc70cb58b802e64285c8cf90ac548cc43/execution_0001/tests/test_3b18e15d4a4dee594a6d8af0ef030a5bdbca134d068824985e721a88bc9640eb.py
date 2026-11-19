import pytest
from httpie.utils import split_iterable

def test_split_iterable_basic():
    """Normal case: mix of items satisfying and not satisfying the key."""
    data = [1, 2, 3, 4, 5]
    left, right = split_iterable(data, lambda x: x % 2 == 0)
    assert left == [2, 4]
    assert right == [1, 3, 5]
    # Ensure original list is unchanged
    assert data == [1, 2, 3, 4, 5]

def test_split_iterable_boundary_cases():
    """Boundary cases: empty iterable, all true, all false."""
    # Empty iterable
    left, right = split_iterable([], lambda x: True)
    assert left == []
    assert right == []

    # All items satisfy the key
    left, right = split_iterable([10, 20, 30], lambda x: x > 5)
    assert left == [10, 20, 30]
    assert right == []

    # No items satisfy the key
    left, right = split_iterable([1, 2, 3], lambda x: x > 5)
    assert left == []
    assert right == [1, 2, 3]

def test_split_iterable_key_raises():
    """Error case: key function raises an exception for a specific item."""
    data = [1, 2, 3]
    def faulty_key(x):
        if x == 2:
            raise ValueError("bad key")
        return x % 2 == 0
    with pytest.raises(ValueError, match="bad key"):
        split_iterable(data, faulty_key)
