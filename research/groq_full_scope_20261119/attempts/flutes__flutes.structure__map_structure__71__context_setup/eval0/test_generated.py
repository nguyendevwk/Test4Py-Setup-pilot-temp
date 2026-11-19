import pytest
from flutes.structure import map_structure

def test_map_structure_nested_collections():
    # Map a function that doubles values over a nested structure
    data = [1, (2, 3), {"a": 4, "b": {5, 6}}]
    result = map_structure(lambda x: x * 2, data)
    assert result == [2, (4, 6), {"a": 8, "b": {10, 12}}]
    # Ensure the original structure types are preserved
    assert isinstance(result, list)
    assert isinstance(result[1], tuple)
    assert isinstance(result[2], dict)
    assert isinstance(result[2]["b"], set)

def test_map_structure_empty_collections():
    # Empty list, tuple, dict, set should return empty structures of same type
    assert map_structure(lambda x: x + 1, []) == []
    assert map_structure(lambda x: x + 1, ()) == ()
    assert map_structure(lambda x: x + 1, {}) == {}
    assert map_structure(lambda x: x + 1, set()) == set()

def test_map_structure_non_collection():
    # When obj is not a collection, fn is applied directly
    assert map_structure(lambda x: x * 3, 7) == 21
    # Ensure that passing a string also applies fn
    assert map_structure(lambda s: s.upper(), "abc") == "ABC"
