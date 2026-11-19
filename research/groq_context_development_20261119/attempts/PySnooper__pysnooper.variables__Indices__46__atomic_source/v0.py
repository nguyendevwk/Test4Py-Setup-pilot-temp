import pytest
from pysnooper.variables import Indices

def test_indices_keys_and_slice_behavior():
    """Indices should return a range slice of the main value and support slicing."""
    indices = Indices()
    # The default slice is slice(None), so _keys should return all indices
    assert indices._keys([10, 20, 30]) == range(3)
    # Slicing the indices should produce a new instance with the updated slice
    sliced = indices[1:3]
    assert isinstance(sliced, Indices)
    # The new slice should be applied when calling _keys
    assert sliced._keys([10, 20, 30]) == range(1, 3)
    # The original instance remains unchanged
    assert indices._keys([10, 20, 30]) == range(3)

def test_indices_deepcopy_and_independence():
    """Each sliced instance should be a deep copy and independent of the original."""
    indices = Indices()
    sliced = indices[0:2]
    # Modify the slice of the sliced instance
    sliced._slice = slice(0, 1)
    # The original should still have its original slice
    assert indices._slice == slice(None)
    # The sliced instance should reflect its own slice
    assert sliced._slice == slice(0, 1)
    # Ensure that the objects are distinct
    assert indices is not sliced

def test_indices_invalid_item_type_raises():
    """Indices.__getitem__ should assert that the key is a slice."""
    indices = Indices()
    with pytest.raises(AssertionError):
        indices[5]  # not a slice, should trigger assertion
