import pytest
from flutes.iterator import MapList

def test_maplist_basic_mapping():
    # Basic mapping: square each element
    original = [1, 2, 3, 4]
    mapped = MapList(lambda x: x * x, original)
    # Check length
    assert len(mapped) == 4
    # Check individual items via indexing
    assert mapped[0] == 1
    assert mapped[1] == 4
    assert mapped[2] == 9
    assert mapped[3] == 16
    # Check iteration yields same sequence
    assert list(mapped) == [1, 4, 9, 16]

def test_maplist_slice_and_iteration():
    # Mapping with a slice and iteration
    original = ['a', 'b', 'c', 'd', 'e']
    mapped = MapList(str.upper, original)
    # Slice returns a list of transformed items
    sliced = mapped[1:4]
    assert sliced == ['B', 'C', 'D']
    # Slicing with step
    sliced_step = mapped[::2]
    assert sliced_step == ['A', 'C', 'E']
    # Iteration over the whole mapped list
    assert list(mapped) == ['A', 'B', 'C', 'D', 'E']

def test_maplist_index_error_on_out_of_range():
    # Accessing an out-of-range index should raise IndexError
    original = [10, 20, 30]
    mapped = MapList(lambda x: x + 1, original)
    with pytest.raises(IndexError):
        _ = mapped[5]
