import pytest
from flutes.structure import reverse_map

def test_reverse_map_basic():
    """Verify that reverse_map returns items sorted by their integer values."""
    mapping = {"apple": 2, "banana": 0, "cherry": 1}
    result = reverse_map(mapping)
    assert result == ["banana", "cherry", "apple"]
    # Ensure that the original mapping is unchanged
    assert mapping == {"apple": 2, "banana": 0, "cherry": 1}

def test_reverse_map_empty():
    """An empty dictionary should produce an empty list."""
    mapping = {}
    result = reverse_map(mapping)
    assert result == []

def test_reverse_map_non_permutation():
    """reverse_map should still sort by the integer values even if they are not a permutation."""
    mapping = {"x": 5, "y": 2, "z": 5}
    result = reverse_map(mapping)
    # The sorted order will place the key with the smallest value first,
    # followed by the others in arbitrary order for equal values.
    assert result[0] == "y"
    assert set(result[1:]) == {"x", "z"}
