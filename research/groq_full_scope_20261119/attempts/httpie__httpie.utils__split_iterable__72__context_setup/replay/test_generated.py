import pytest
from httpie.utils import split_iterable

def test_split_iterable_basic():
    """Verify that items are correctly partitioned based on a simple predicate."""
    data = [1, 2, 3, 4, 5]
    even, odd = split_iterable(data, lambda x: x % 2 == 0)
    assert even == [2, 4]
    assert odd == [1, 3, 5]
    # Ensure original list is untouched
    assert data == [1, 2, 3, 4, 5]

def test_split_iterable_empty_iterable():
    """When given an empty iterable, both result lists should be empty."""
    empty = []
    left, right = split_iterable(empty, lambda x: True)
    assert left == []
    assert right == []

def test_split_iterable_key_raises_exception():
    """If the key function raises an exception, split_iterable should propagate it."""
    data = [1, 2, 3]
    def bad_key(x):
        if x == 2:
            raise ValueError("bad key")
        return True
    with pytest.raises(ValueError, match="bad key"):
        split_iterable(data, bad_key)
