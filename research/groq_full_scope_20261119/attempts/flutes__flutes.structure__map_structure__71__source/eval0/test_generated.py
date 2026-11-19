import pytest
from flutes.structure import map_structure

def test_map_structure_nested_collections():
    # Map a simple function over a nested structure containing lists, tuples, dicts, and sets
    data = {
        "numbers": [1, 2, 3],
        "info": ("a", {"b": 4, "c": [5, 6]}),
        "empty_set": set(),
    }
    result = map_structure(lambda x: x * 10 if isinstance(x, int) else x, data)
    assert result == {
        "numbers": [10, 20, 30],
        "info": ("a", {"b": 40, "c": [50, 60]}),
        "empty_set": set(),
    }

def test_map_structure_empty_collections():
    # Mapping over empty collections should preserve the type and remain empty
    assert map_structure(lambda x: x, []) == []
    assert map_structure(lambda x: x, ()) == ()
    assert map_structure(lambda x: x, {}) == {}
    assert map_structure(lambda x: x, set()) == set()

def test_map_structure_non_collection_argument():
    # When the argument is not a collection, the function is applied directly
    assert map_structure(lambda x: x + 1, 5) == 6
    with pytest.raises(TypeError):
        # The function expects an integer, but a string is passed, causing a TypeError
        map_structure(lambda x: x + 1, "not an int")
