import pytest
from pysnooper.variables import Indices

def test_indices_keys_and_slice(tmp_path):
    # Normal behavior: _keys returns a range over the list length
    indices = Indices()
    main_list = [10, 20, 30, 40]
    keys = list(indices._keys(main_list))
    assert keys == [0, 1, 2, 3], "Indices._keys should return all indices of the list"

    # Slicing: __getitem__ returns a new Indices with updated slice
    sliced = indices[1:3]
    assert isinstance(sliced, Indices), "Result of slicing should be an Indices instance"
    sliced_keys = list(sliced._keys(main_list))
    assert sliced_keys == [1, 2], "Sliced indices should match the slice range"

    # Ensure the original indices object is unchanged
    original_keys = list(indices._keys(main_list))
    assert original_keys == [0, 1, 2, 3], "Original Indices should remain unchanged after slicing"

def test_indices_slice_default_behavior(tmp_path):
    # When no slice is provided, _slice defaults to slice(None)
    indices = Indices()
    main_list = [5, 15, 25]
    # Default slice should cover all indices
    default_keys = list(indices._keys(main_list))
    assert default_keys == [0, 1, 2], "Default slice should include all indices"

    # Explicit full slice should produce the same result
    full_slice = indices[:]
    full_keys = list(full_slice._keys(main_list))
    assert full_keys == [0, 1, 2], "Explicit full slice should match default behavior"

def test_indices_invalid_item_type(tmp_path):
    indices = Indices()
    # __getitem__ expects a slice; passing an int should raise an AssertionError
    with pytest.raises(AssertionError):
        _ = indices[1]  # type: ignore[arg-type]
