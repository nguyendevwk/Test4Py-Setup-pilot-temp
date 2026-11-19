import pytest
from httpie.utils import split_iterable

def test_split_iterable_basic():
    """Verify that items are correctly partitioned based on the key function."""
    data = [1, 2, 3, 4, 5]
    # key: even numbers
    left, right = split_iterable(data, lambda x: x % 2 == 0)
    assert left == [2, 4], f"Expected evens in left, got {left}"
    assert right == [1, 3, 5], f"Expected odds in right, got {right}"
    # Ensure original list is unchanged
    assert data == [1, 2, 3, 4, 5]

def test_split_iterable_empty_iterable():
    """Splitting an empty iterable should return two empty lists."""
    left, right = split_iterable([], lambda x: True)
    assert left == [], "Left should be empty for empty input"
    assert right == [], "Right should be empty for empty input"

def test_split_iterable_key_exception():
    """If the key function raises an exception, it should propagate."""
    data = [1, 2, 3]
    def bad_key(x):
        if x == 2:
            raise ValueError("bad key")
        return True
    with pytest.raises(ValueError, match="bad key"):
        split_iterable(data, bad_key)
