import pytest
from flutes.structure import map_structure

def test_map_structure_nested_collections():
    # Map a function that doubles numbers over a nested structure
    data = [1, (2, 3), {"a": 4, "b": {5, 6}}, [7]]
    result = map_structure(lambda x: x * 2, data)
    assert result == [2, (4, 6), {"a": 8, "b": {10, 12}}, [14]]
    # Ensure the original structure types are preserved
    assert isinstance(result, list)
    assert isinstance(result[1], tuple)
    assert isinstance(result[2], dict)
    assert isinstance(result[2]["b"], set)
    assert isinstance(result[3], list)

def test_map_structure_empty_and_singleton():
    # Empty list should return an empty list
    assert map_structure(lambda x: x + 1, []) == []
    # Empty dict should return an empty dict
    assert map_structure(lambda x: x + 1, {}) == {}
    # Empty set should return an empty set
    assert map_structure(lambda x: x + 1, set()) == set()
    # Single integer should be transformed directly
    assert map_structure(lambda x: x + 1, 10) == 11

def test_map_structure_non_collection_and_no_map_flag():
    # Objects with the special no-map attribute should be returned unchanged
    class NoMap:
        __dict__ = {"__no_map__": True}
    obj = NoMap()
    # Attach the special attribute to trigger the early return
    setattr(obj, "--no-map--", True)
    assert map_structure(lambda x: x * 2, obj) is obj

    # Objects that are not collections are passed directly to fn
    assert map_structure(lambda x: x * 3, 5) == 15
