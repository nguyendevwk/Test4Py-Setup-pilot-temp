import pytest
from copy import deepcopy
from pysnooper.variables import Indices

def test_indices_slice_basic():
    """Indices should return a new instance with the updated slice."""
    indices = Indices()
    sliced = indices[1:4]
    # Ensure a new object is returned
    assert sliced is not indices
    # The slice should be stored correctly
    assert sliced._slice == slice(1, 4)
    # The underlying _keys method should reflect the slice
    assert list(sliced._keys([10, 20, 30, 40, 50])) == [1, 2, 3]

def test_indices_slice_boundary():
    """Indices should handle boundary conditions correctly."""
    indices = Indices()
    sliced = indices[:3]
    # Slice from start to 3
    assert sliced._slice == slice(None, 3)
    assert list(sliced._keys([1, 2, 3, 4, 5])) == [0, 1, 2]
    # Slice with step
    sliced_step = indices[::2]
    assert sliced_step._slice == slice(None, None, 2)
    assert list(sliced_step._keys([10, 20, 30, 40, 50])) == [0, 2, 4]

def test_indices_invalid_item():
    """Indices.__getitem__ should assert that the key is a slice."""
    indices = Indices()
    with pytest.raises(AssertionError):
        _ = indices[5]  # not a slice
