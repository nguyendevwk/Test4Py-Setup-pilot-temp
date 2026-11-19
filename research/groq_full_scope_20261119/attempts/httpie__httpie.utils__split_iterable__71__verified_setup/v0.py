import pytest
from httpie.utils import split_iterable

def test_split_iterable_basic():
    # Basic split: separate even and odd numbers
    data = [1, 2, 3, 4, 5]
    left, right = split_iterable(data, lambda x: x % 2 == 0)
    assert left == [2, 4], f"Expected evens in left, got {left}"
    assert right == [1, 3, 5], f"Expected odds in right, got {right}"

def test_split_iterable_generator_and_empty():
    # Test with a generator and an empty iterable
    gen = (x for x in range(3))  # yields 0,1,2
    left, right = split_iterable(gen, lambda x: x > 1)
    assert left == [2], f"Expected [2] in left, got {left}"
    assert right == [0, 1], f"Expected [0,1] in right, got {right}"
    # Empty iterable should return two empty lists
    empty_left, empty_right = split_iterable([], lambda x: True)
    assert empty_left == []
    assert empty_right == []

def test_split_iterable_key_exception_propagates():
    # If the key function raises an exception, it should propagate
    data = [1, 2, 3]
    def bad_key(x):
        if x == 2:
            raise ValueError("bad key")
        return True
    with pytest.raises(ValueError, match="bad key"):
        split_iterable(data, bad_key)
