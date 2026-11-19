import pytest
from httpie.utils import split_iterable

def test_split_iterable_even_odd():
    data = [1, 2, 3, 4, 5]
    left, right = split_iterable(data, lambda x: x % 2 == 0)
    assert left == [2, 4]
    assert right == [1, 3, 5]
    # Ensure original list is unchanged
    assert data == [1, 2, 3, 4, 5]

def test_split_iterable_empty():
    empty = []
    left, right = split_iterable(empty, lambda x: True)
    assert left == []
    assert right == []

def test_split_iterable_key_error():
    data = [1, 2, 3]
    def bad_key(x):
        if x == 2:
            raise ValueError("bad key")
        return True
    with pytest.raises(ValueError, match="bad key"):
        split_iterable(data, bad_key)
