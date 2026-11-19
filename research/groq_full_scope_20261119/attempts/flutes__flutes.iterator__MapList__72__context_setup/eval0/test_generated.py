import pytest
from flutes.iterator import MapList

def test_maplist_basic_mapping_and_length():
    # Basic mapping: square each element
    data = [1, 2, 3, 4]
    ml = MapList(lambda x: x * x, data)
    # Length should match underlying list
    assert len(ml) == 4
    # Indexing returns transformed value
    assert ml[0] == 1
    assert ml[1] == 4
    assert ml[2] == 9
    assert ml[3] == 16
    # Iteration yields transformed values in order
    assert list(iter(ml)) == [1, 4, 9, 16]

def test_maplist_slice_and_iteration_order():
    # Slice returns a list of transformed values
    data = [10, 20, 30, 40, 50]
    ml = MapList(lambda x: x // 10, data)
    sliced = ml[1:4]          # should transform 20,30,40
    assert sliced == [2, 3, 4]
    # Slicing with step
    sliced_step = ml[::2]     # 10,30,50 -> 1,3,5
    assert sliced_step == [1, 3, 5]
    # Iteration over the whole MapList
    assert list(ml) == [1, 2, 3, 4, 5]

def test_maplist_error_conditions_and_boundary():
    # Out-of-range index should raise IndexError
    ml = MapList(lambda x: x * 2, [1, 2])
    with pytest.raises(IndexError):
        _ = ml[5]
    # Negative indices work as per list semantics
    assert ml[-1] == 4
    # Slicing beyond bounds returns transformed values up to the end
    assert ml[1:10] == [4]
    # Passing a non-sequence to constructor should raise TypeError
    with pytest.raises(TypeError):
        MapList(lambda x: x, 123)  # 123 is not a Sequence
