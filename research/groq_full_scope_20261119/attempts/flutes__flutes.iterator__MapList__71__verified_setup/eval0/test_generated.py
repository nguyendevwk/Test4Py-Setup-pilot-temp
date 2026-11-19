import pytest
from flutes.iterator import MapList

def test_maplist_normal_mapping_and_iteration():
    # Normal mapping: square each element
    original = [1, 2, 3, 4]
    ml = MapList(lambda x: x * x, original)
    # __len__ should match original list length
    assert len(ml) == 4
    # __getitem__ with int should apply function
    assert ml[2] == 9
    # Iteration should yield transformed values
    assert list(ml) == [1, 4, 9, 16]
    # Ensure original list is unchanged
    assert original == [1, 2, 3, 4]

def test_maplist_slice_and_index_behavior():
    # Test slice returns a list of transformed elements
    original = [10, 20, 30, 40, 50]
    ml = MapList(lambda x: x // 10, original)
    # Slice from index 1 to 4 (exclusive)
    sliced = ml[1:4]
    assert isinstance(sliced, list)
    assert sliced == [2, 3, 4]
    # Negative indices should work as in normal list
    assert ml[-1] == 5
    # Full slice should return all transformed elements
    assert ml[:] == [1, 2, 3, 4, 5]

def test_maplist_error_on_out_of_range_and_invalid_func():
    # Out-of-range index should raise IndexError
    ml = MapList(lambda x: x * 2, [1, 2, 3])
    with pytest.raises(IndexError):
        _ = ml[5]
    # Passing a non-callable as func should raise TypeError when called
    with pytest.raises(TypeError):
        # The constructor accepts any callable, but calling __getitem__ will fail
        ml_bad = MapList("not a function", [1, 2])
        _ = ml_bad[0]
