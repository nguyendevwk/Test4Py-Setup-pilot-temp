import pytest
from pysnooper.variables import Indices

def test_indices_slicing_and_deepcopy(tmp_path):
    # Create an instance of Indices
    indices = Indices()
    # Original slice should be slice(None)
    assert indices._slice == slice(None)

    # Apply a slice to get a new Indices instance
    sliced = indices[1:4:2]
    # The original instance remains unchanged
    assert indices._slice == slice(None)
    # The sliced instance has the new slice
    assert sliced._slice == slice(1, 4, 2)

    # Test that _keys returns the correct range slice
    data = ['a', 'b', 'c', 'd', 'e']
    # Using the sliced instance
    result = list(sliced._keys(data))
    # Should return indices 1 and 3
    assert result == [1, 3]

    # Ensure deepcopy works: modifying the slice of the new instance
    # should not affect the original
    sliced._slice = slice(0, 2)
    assert sliced._slice == slice(0, 2)
    assert indices._slice == slice(None)

def test_indices_non_slice_error():
    indices = Indices()
    # __getitem__ should assert that the key is a slice
    with pytest.raises(AssertionError):
        indices[5]  # not a slice

def test_indices_with_empty_and_full_slice(tmp_path):
    indices = Indices()
    data = [10, 20, 30]
    # Full slice should return all indices
    full = indices[:]
    assert list(full._keys(data)) == [0, 1, 2]
    # Empty slice should return empty list
    empty = indices[1:1]
    assert list(empty._keys(data)) == []
