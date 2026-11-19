import pytest
from pysnooper.variables import Indices

def test_indices_slice_and_keys(tmp_path):
    # Create a sample list and an Indices instance
    data = [10, 20, 30, 40, 50]
    idx = Indices()
    # Verify that _keys returns all indices for the full slice
    assert list(idx._keys(data)) == list(range(len(data)))
    # Apply a slice to get a subset of indices
    sliced_idx = idx[1:4:2]  # should correspond to indices 1 and 3
    assert isinstance(sliced_idx, Indices)
    # Ensure the slice is stored correctly
    assert sliced_idx._slice == slice(1, 4, 2)
    # Verify that _keys on the sliced instance returns the correct subset
    assert list(sliced_idx._keys(data)) == [1, 3]
    # Ensure the original idx remains unchanged
    assert idx._slice == slice(None)

def test_indices_deepcopy_behavior(tmp_path):
    idx = Indices()
    # Create a sliced copy
    sliced_idx = idx[0:3]
    # Mutate the slice of the copy
    sliced_idx._slice = slice(2, 5)
    # The original should still have its original slice
    assert idx._slice == slice(None)
    # The mutated copy should reflect the new slice
    assert sliced_idx._slice == slice(2, 5)

def test_indices_invalid_item_raises(tmp_path):
    idx = Indices()
    # Passing a non-slice should raise an AssertionError
    with pytest.raises(AssertionError):
        _ = idx[5]  # int instead of slice
