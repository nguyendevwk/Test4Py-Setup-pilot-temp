import pytest
from flutes.iterator import MapList

def test_maplist_basic_mapping_and_length():
    # MapList should apply the function lazily and report correct length
    data = [1, 2, 3, 4]
    ml = MapList(lambda x: x * 10, data)
    assert len(ml) == 4
    # Individual items are transformed correctly
    assert ml[0] == 10
    assert ml[1] == 20
    assert ml[2] == 30
    assert ml[3] == 40
    # Iteration yields transformed values in order
    assert list(ml) == [10, 20, 30, 40]

def test_maplist_slice_and_indexing_behavior():
    # Slice should return a list of transformed elements
    data = ['a', 'b', 'c', 'd']
    ml = MapList(str.upper, data)
    assert ml[1:3] == ['B', 'C']
    # Negative indices and full slice
    assert ml[-1] == 'D'
    assert ml[:] == ['A', 'B', 'C', 'D']

def test_maplist_error_on_invalid_index():
    # Accessing an out-of-range index should raise IndexError
    data = [5, 6]
    ml = MapList(lambda x: x + 1, data)
    with pytest.raises(IndexError):
        _ = ml[5]
    # Slicing beyond bounds should not raise, just return available items
    assert ml[0:10] == [6, 7]
