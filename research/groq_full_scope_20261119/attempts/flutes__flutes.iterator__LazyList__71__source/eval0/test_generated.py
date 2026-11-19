import pytest
from flutes.iterator import LazyList

def test_lazy_list_single_access():
    """Accessing an element triggers lazy fetching up to that index."""
    source = (x for x in range(5))  # generator
    ll = LazyList(source)
    # Initially list is empty
    assert ll.list == []
    # Access index 2, should fetch elements 0,1,2
    assert ll[2] == 2
    assert ll.list == [0, 1, 2]
    # Access index 4, should fetch remaining elements
    assert ll[4] == 4
    assert ll.list == [0, 1, 2, 3, 4]
    # After exhaustion, accessing any index returns from cached list
    assert ll[0] == 0
    assert ll[3] == 3

def test_lazy_list_slice_beyond_end():
    """Slicing beyond the iterable's end should not raise and should return all elements."""
    source = [10, 20, 30]
    ll = LazyList(source)
    # Slice beyond the end
    sliced = ll[1:10]
    assert sliced == [20, 30]
    # The internal list should now contain all elements
    assert ll.list == [10, 20, 30]
    # Further slicing should return the same result
    assert ll[0:5] == [10, 20, 30]

def test_lazy_list_len_before_exhaustion():
    """Calling __len__ before the iterable is exhausted raises TypeError."""
    source = iter(range(3))
    ll = LazyList(source)
    with pytest.raises(TypeError, match="__len__ is not available before the iterable is depleted"):
        len(ll)
    # After exhausting the iterable, len should work
    _ = ll[2]  # triggers exhaustion
    assert len(ll) == 3
