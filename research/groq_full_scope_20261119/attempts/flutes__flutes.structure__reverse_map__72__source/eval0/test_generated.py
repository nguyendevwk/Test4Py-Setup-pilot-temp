import pytest
from flutes.structure import reverse_map

def test_reverse_map_basic_ordering():
    """Verify that reverse_map returns items sorted by their integer ids."""
    mapping = {"apple": 2, "banana": 0, "cherry": 1}
    result = reverse_map(mapping)
    assert result == ["banana", "cherry", "apple"]
    # Ensure the original mapping is unchanged
    assert mapping == {"apple": 2, "banana": 0, "cherry": 1}

def test_reverse_map_empty_dict():
    """reverse_map should return an empty list when given an empty dictionary."""
    assert reverse_map({}) == []

def test_reverse_map_non_contiguous_ids():
    """reverse_map should still sort by id even if ids are not contiguous."""
    mapping = {"x": 10, "y": 5, "z": 7}
    result = reverse_map(mapping)
    assert result == ["y", "z", "x"]
    # The length of the result should match the number of items
    assert len(result) == 3
