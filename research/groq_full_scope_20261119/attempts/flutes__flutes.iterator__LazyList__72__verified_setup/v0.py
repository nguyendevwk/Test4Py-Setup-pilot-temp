import pytest
from flutes.iterator import LazyList


def test_lazy_list_single_access_and_iteration():
    """Accessing an element triggers lazy fetching and iteration works."""
    source = (i for i in range(5))  # generator
    ll = LazyList(source)

    # Access first element; should trigger fetch until index 0
    assert ll[0] == 0
    # The internal list should now contain only the first element
    assert ll.list == [0]

    # Access a later element; should fetch up to that index
    assert ll[3] == 3
    assert ll.list == [0, 1, 2, 3]

    # Iterate over the remaining elements; should consume the rest
    remaining = list(ll)
    assert remaining == [4]
    # After iteration, the list should be fully populated
    assert ll.list == [0, 1, 2, 3, 4]
    # The iterator should now be exhausted
    assert ll.exhausted is True


def test_lazy_list_slice_beyond_end_and_negative_index():
    """Slicing beyond the end should return all available items without error."""
    source = [10, 20, 30]
    ll = LazyList(source)

    # Slice that goes beyond the length; should fetch all items
    slice_result = ll[1:10]
    assert slice_result == [20, 30]
    # The internal list should now contain all items
    assert ll.list == [10, 20, 30]
    assert ll.exhausted is True

    # Negative index should be treated as None (fetch all)
    ll2 = LazyList([1, 2, 3])
    assert ll2[-1] == 1  # negative index triggers fetch until None
    assert ll2.list == [1, 2, 3]
    assert ll2.exhausted is True


def test_lazy_list_len_before_exhaustion_raises_type_error():
    """Calling __len__ before the iterable is exhausted should raise TypeError."""
    source = (i for i in range(3))
    ll = LazyList(source)

    # Access an element to partially consume the iterator
    _ = ll[0]
    # __len__ should still raise TypeError because not all items fetched
    with pytest.raises(TypeError, match="__len__ is not available before the iterable is depleted"):
        len(ll)

    # Exhaust the iterator fully
    list(ll)
    # Now __len__ should return the correct length
    assert len(ll) == 3
