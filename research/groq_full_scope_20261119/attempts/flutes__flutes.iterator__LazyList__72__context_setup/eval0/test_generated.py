import pytest
from flutes.iterator import LazyList

def test_lazy_list_basic_access_and_iteration():
    # Create a LazyList from a simple iterable
    source = (x for x in range(5))
    lazy = LazyList(source)

    # Access by index should trigger fetching up to that index
    assert lazy[2] == 2
    # The internal list should now contain elements 0,1,2
    assert lazy.list == [0, 1, 2]

    # Iterating over the LazyList should continue fetching remaining items
    items = list(lazy)
    assert items == [0, 1, 2, 3, 4]
    # After exhaustion, the internal list should contain all elements
    assert lazy.list == [0, 1, 2, 3, 4]
    # Subsequent iteration should use the cached list
    assert list(lazy) == [0, 1, 2, 3, 4]

def test_lazy_list_slice_and_negative_index():
    # Use a finite iterable
    lazy = LazyList(range(10))

    # Slice that goes beyond the current list length should fetch all needed items
    slice_result = lazy[3:8]
    assert slice_result == [3, 4, 5, 6, 7]
    # The internal list should now contain elements up to index 7
    assert lazy.list == list(range(8))

    # Negative index should fetch until the end of the iterable
    last_item = lazy[-1]
    assert last_item == 9
    # After fetching the last element, the list should be complete
    assert lazy.list == list(range(10))
    # Accessing the same negative index again should not raise
    assert lazy[-1] == 9

def test_lazy_list_len_and_error_behavior():
    # Create a LazyList from an infinite generator
    def infinite_gen():
        i = 0
        while True:
            yield i
            i += 1
    lazy = LazyList(infinite_gen())

    # __len__ should raise TypeError before exhaustion
    with pytest.raises(TypeError, match="__len__ is not available before the iterable is depleted"):
        len(lazy)

    # Accessing an index should fetch up to that point
    assert lazy[5] == 5
    # Now the list is partially fetched but not exhausted
    with pytest.raises(TypeError):
        len(lazy)

    # Exhaust the iterator by converting to list
    _ = list(lazy)
    # After exhaustion, __len__ should return the correct length
    assert len(lazy) == 1000  # the generator yields 1000 items in this test
