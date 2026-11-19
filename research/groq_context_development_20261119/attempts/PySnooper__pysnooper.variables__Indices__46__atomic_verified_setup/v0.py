import pytest
from pysnooper.variables import Indices

def test_indices_slice_and_deepcopy(tmp_path):
    # Create an Indices instance and slice it
    indices = Indices()
    sliced = indices[1:3]
    # The slice should be stored correctly
    assert sliced._slice == slice(1, 3)
    # The original should remain unchanged
    assert indices._slice == slice(None)
    # Ensure deepcopy: modifying sliced does not affect original
    sliced._slice = slice(0, 1)
    assert indices._slice == slice(None)

def test_indices_keys_output():
    indices = Indices()
    # Apply a slice and get keys for a list
    sliced = indices[1:4]
    keys = list(sliced._keys([10, 20, 30, 40, 50]))
    # Should return indices 1,2,3
    assert keys == [1, 2, 3]
    # Without slice, should return all indices
    all_keys = list(indices._keys([10, 20, 30]))
    assert all_keys == [0, 1, 2]

def test_indices_getitem_invalid_type():
    indices = Indices()
    # __getitem__ should assert that the key is a slice
    with pytest.raises(AssertionError):
        _ = indices[5]  # int is not a slice
