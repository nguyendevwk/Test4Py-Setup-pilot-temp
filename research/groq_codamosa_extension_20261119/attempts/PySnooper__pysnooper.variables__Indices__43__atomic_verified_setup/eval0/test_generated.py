import pytest
from pysnooper.variables import Indices

def test_indices_keys_basic():
    """Indices should return all indices of a list when no slice is applied."""
    indices = Indices()
    main_value = [10, 20, 30]
    # _keys should produce a range of indices
    assert list(indices._keys(main_value)) == [0, 1, 2]
    # The slice is the default slice(None), so __getitem__ with slice(None) returns the same
    sliced = indices[indices._slice]
    assert isinstance(sliced, Indices)
    assert list(sliced._keys(main_value)) == [0, 1, 2]
    # Ensure deepcopy created a new object
    assert sliced is not indices

def test_indices_slice_boundary():
    """Indices should correctly handle slice boundaries and produce the expected subset."""
    indices = Indices()
    main_value = ['a', 'b', 'c', 'd', 'e']
    # Slice from index 1 to 4 (exclusive)
    sliced = indices[1:4]
    assert isinstance(sliced, Indices)
    assert list(sliced._keys(main_value)) == [1, 2, 3]
    # Slice with step
    sliced_step = indices[::2]
    assert list(sliced_step._keys(main_value)) == [0, 2, 4]
    # Slice beyond bounds should not raise and should clip
    sliced_over = indices[3:10]
    assert list(sliced_over._keys(main_value)) == [3, 4]
    # Negative indices
    sliced_neg = indices[-3:-1]
    assert list(sliced_neg._keys(main_value)) == [2, 3]

def test_indices_invalid_item():
    """Indices.__getitem__ should raise an AssertionError when the key is not a slice."""
    indices = Indices()
    with pytest.raises(AssertionError):
        _ = indices[0]          # int key
    with pytest.raises(AssertionError):
        _ = indices['a']        # non-slice key
    with pytest.raises(AssertionError):
        _ = indices[(1, 2)]     # tuple key
