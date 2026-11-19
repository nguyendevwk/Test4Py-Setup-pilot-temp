import pytest
from flutes.iterator import LazyList

def test_lazy_list_basic_access_and_iteration():
    # Create a LazyList from a generator that yields 0..4
    gen = (i for i in range(5))
    ll = LazyList(gen)

    # Accessing an element triggers fetching up to that index
    assert ll[2] == 2
    # The internal list should now contain the first three elements
    assert ll.list == [0, 1, 2]

    # Iterating over the LazyList consumes the remaining elements
    result = list(ll)
    assert result == [0, 1, 2, 3, 4]
    # After exhaustion, the internal list should be complete
    assert ll.list == [0, 1, 2, 3, 4]
    # Subsequent iteration should use the cached list
    assert list(ll) == [0, 1, 2, 3, 4]

def test_lazy_list_len_before_exhaustion_raises_type_error():
    # LazyList from a finite iterable
    ll = LazyList(range(3))
    # Access one element to start fetching
    assert ll[0] == 0
    # __len__ should raise TypeError until the iterable is fully consumed
    with pytest.raises(TypeError, match="__len__ is not available before the iterable is depleted"):
        len(ll)

    # Exhaust the iterable
    list(ll)
    # Now __len__ should return the correct length
    assert len(ll) == 3

def test_lazy_list_slice_and_negative_index_behavior():
    # LazyList from a generator that yields 10..14
    ll = LazyList(i for i in range(10, 15))

    # Slice up to stop index 12 (exclusive)
    slice_result = ll[10:12]
    assert slice_result == [10, 11]
    # The internal list should contain elements up to index 11
    assert ll.list == [10, 11]

    # Accessing a negative index should fetch all elements
    assert ll[-1] == 14
    # After accessing negative index, the list should be fully populated
    assert ll.list == [10, 11, 12, 13, 14]
    # Slicing beyond the end should return all available elements
    assert ll[12:20] == [12, 13, 14]
