import pytest
from pysnooper.variables import Indices

def test_indices_slicing_and_deepcopy(tmp_path):
    # Create an Indices instance and verify that slicing returns a new instance
    indices = Indices()
    # Original slice should be slice(None)
    assert indices._slice == slice(None)

    # Apply a slice that selects the first two indices
    sliced = indices[0:2]
    # The sliced instance should have the new slice
    assert sliced._slice == slice(0, 2, None)
    # The original instance should remain unchanged
    assert indices._slice == slice(None)

    # Verify that deepcopy was performed by checking identity of internal slice
    assert sliced is not indices
    assert sliced._slice is not indices._slice

    # Test that _keys returns the correct range of indices for a sample list
    sample = [10, 20, 30, 40]
    # For the sliced instance, _keys should return range(0, 2)
    assert list(sliced._keys(sample)) == [0, 1]
    # For the original instance, _keys should return all indices
    assert list(indices._keys(sample)) == [0, 1, 2, 3]

def test_indices_invalid_item_raises():
    indices = Indices()
    # __getitem__ should assert that the item is a slice
    with pytest.raises(AssertionError):
        _ = indices[5]  # not a slice

def test_indices_slice_edge_cases():
    indices = Indices()
    sample = ['a', 'b', 'c', 'd', 'e']

    # Slice with step and negative indices
    sliced = indices[1:4:2]
    assert sliced._slice == slice(1, 4, 2)
    assert list(sliced._keys(sample)) == [1, 3]

    # Slice that goes beyond the list length
    sliced_over = indices[3:10]
    assert sliced_over._slice == slice(3, 10, None)
    assert list(sliced_over._keys(sample)) == [3, 4]

    # Slice that selects nothing
    sliced_none = indices[5:5]
    assert sliced_none._slice == slice(5, 5, None)
    assert list(sliced_none._keys(sample)) == []
