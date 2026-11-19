import pytest
from flutes.iterator import LazyList

def test_lazy_list_basic_access_and_iteration():
    # Create a LazyList from a finite iterable
    source = (x for x in range(5))
    lazy = LazyList(source)

    # Access elements by index; should trigger lazy fetching
    assert lazy[0] == 0
    assert lazy[4] == 4

    # After accessing the last element, the iterable is exhausted
    with pytest.raises(TypeError):
        len(lazy)  # __len__ should raise before exhaustion

    # Now the list is fully populated; len should work
    assert len(lazy) == 5

    # Iterating over the LazyList should yield the same elements
    assert list(lazy) == [0, 1, 2, 3, 4]

def test_lazy_list_slice_and_negative_index():
    # Use a generator that yields more than needed
    source = (x for x in range(10))
    lazy = LazyList(source)

    # Slice that goes beyond the current fetched range; should fetch until stop
    sliced = lazy[2:7]
    assert sliced == [2, 3, 4, 5, 6]

    # Negative index should fetch until the element is available
    assert lazy[-1] == 9  # last element of the original iterable

    # After accessing negative index, the list should be fully populated
    assert len(lazy) == 10

def test_lazy_list_error_behavior_and_exhaustion():
    # Create a LazyList from an empty iterable
    lazy = LazyList(iter([]))

    # Accessing any index should raise IndexError
    with pytest.raises(IndexError):
        _ = lazy[0]

    # Slicing an empty iterable should return an empty list
    assert lazy[0:5] == []

    # After confirming exhaustion, len should return 0
    assert len(lazy) == 0

    # Iterating over an exhausted LazyList should yield nothing
    assert list(lazy) == []
