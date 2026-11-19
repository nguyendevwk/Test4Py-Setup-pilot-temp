import pytest
from pysnooper.variables import Indices

def test_indices_slice_and_keys():
    """Indices should correctly slice and return index ranges."""
    # Create an Indices instance and slice it
    idx = Indices()
    sliced = idx[1:4]  # should represent indices 1,2,3
    # The sliced instance should have its own _slice attribute
    assert sliced._slice == slice(1, 4, None)
    # _keys should return the correct range for a given main_value
    main = [10, 20, 30, 40, 50]
    expected = list(range(1, 4))  # indices 1,2,3
    assert sliced._keys(main) == expected

def test_indices_full_slice_and_deepcopy():
    """Slicing with full slice should preserve all indices and deepcopy should be independent."""
    idx = Indices()
    full = idx[:]  # full slice
    # full slice should be equivalent to slice(None)
    assert full._slice == slice(None)
    main = ['a', 'b', 'c']
    # _keys should return all indices
    assert full._keys(main) == [0, 1, 2]
    # Ensure deepcopy creates a separate object
    assert full is not idx
    # Modifying the slice of the new object should not affect the original
    full._slice = slice(0, 1)
    assert idx._slice == slice(None)

def test_indices_invalid_item_type():
    """Indices.__getitem__ should assert that the key is a slice."""
    idx = Indices()
    with pytest.raises(AssertionError):
        _ = idx[5]          # integer key
    with pytest.raises(AssertionError):
        _ = idx['a']        # string key
    with pytest.raises(AssertionError):
        _ = idx[None]       # None key
