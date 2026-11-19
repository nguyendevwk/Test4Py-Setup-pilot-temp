import pytest
from pysnooper.variables import Indices

def test_indices_slice_and_keys():
    """Verify that slicing an Indices instance returns a new instance with the
    correct slice and that _keys yields the expected range."""
    indices = Indices()
    sliced = indices[2:5]
    # The sliced instance should be a different object
    assert sliced is not indices
    # The slice attribute should be set correctly
    assert sliced._slice == slice(2, 5)
    # _keys should return a range object that respects the slice
    assert list(sliced._keys([10, 20, 30, 40, 50, 60])) == [2, 3, 4]

def test_indices_deepcopy_independence():
    """Ensure that deepcopying an Indices instance preserves its state and
    that subsequent modifications do not affect the original."""
    original = Indices()
    original._slice = slice(1, 3)
    copied = deepcopy(original)
    # Changing the slice on the copy should not affect the original
    copied._slice = slice(0, 2)
    assert original._slice == slice(1, 3)
    assert copied._slice == slice(0, 2)

def test_indices_invalid_item_type():
    """Accessing an Indices instance with a non-slice should raise an AssertionError."""
    indices = Indices()
    with pytest.raises(AssertionError):
        _ = indices[5]  # int is not a slice
