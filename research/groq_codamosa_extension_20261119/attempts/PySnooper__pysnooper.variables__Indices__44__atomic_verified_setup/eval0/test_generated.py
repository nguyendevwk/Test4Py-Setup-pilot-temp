import pytest
from pysnooper.variables import Indices

def test_indices_slice_and_keys(tmp_path):
    # Create an Indices instance and verify default slice
    idx = Indices()
    assert idx._slice == slice(None)
    # Default _keys should return full range
    assert list(idx._keys([10, 20, 30])) == [0, 1, 2]

    # Apply a slice and check that a new instance is returned
    sliced = idx[1:3]
    assert isinstance(sliced, Indices)
    assert sliced is not idx  # ensure a new object
    # The new slice should be reflected in _keys
    assert list(sliced._keys([10, 20, 30])) == [1, 2]

def test_indices_slice_boundary_conditions(tmp_path):
    # Test slicing with step and negative indices
    idx = Indices()
    sliced = idx[::2]  # step of 2
    assert list(sliced._keys([10, 20, 30, 40, 50])) == [0, 2, 4]

    sliced_neg = idx[-3:-1]
    assert list(sliced_neg._keys([10, 20, 30, 40, 50])) == [2, 3]

def test_indices_invalid_item_raises():
    idx = Indices()
    with pytest.raises(AssertionError):
        idx[5]  # not a slice, should trigger assertion
