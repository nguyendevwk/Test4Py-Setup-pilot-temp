import pytest
from flutes.iterator import LazyList

def test_lazy_list_single_access():
    """Accessing a single element should trigger lazy fetching up to that index."""
    data = (x for x in range(5))  # generator
    ll = LazyList(data)
    # Initially the underlying list is empty
    assert ll.list == []
    # Access element at index 2
    assert ll[2] == 2
    # Now the list should contain elements 0,1,2
    assert ll.list == [0, 1, 2]
    # Subsequent access to an earlier index should not trigger more fetching
    assert ll[1] == 1
    assert ll.list == [0, 1, 2]

def test_lazy_list_slice_beyond_end():
    """Slicing beyond the end should fetch all remaining elements and stop gracefully."""
    data = iter([10, 20, 30])
    ll = LazyList(data)
    # Slice that goes beyond the available items
    result = ll[1:5]
    assert result == [20, 30]
    # After slicing, the list should contain all items
    assert ll.list == [10, 20, 30]
    # The iterator should now be exhausted
    assert ll.exhausted is True
    # Further slicing should return an empty list
    assert ll[5:10] == []

def test_lazy_list_len_before_exhaustion():
    """Calling len on a LazyList before it is fully consumed should raise TypeError."""
    data = iter(range(3))
    ll = LazyList(data)
    with pytest.raises(TypeError, match="__len__ is not available before the iterable is depleted"):
        len(ll)
    # After exhausting the iterator, len should work
    list(ll)  # consume all items
    assert len(ll) == 3
