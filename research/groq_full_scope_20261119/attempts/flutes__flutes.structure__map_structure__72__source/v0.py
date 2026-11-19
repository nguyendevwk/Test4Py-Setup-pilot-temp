import pytest
from flutes.structure import map_structure

def test_map_structure_basic_types():
    # Mapping over a simple list of integers
    result = map_structure(lambda x: x * 2, [1, 2, 3])
    assert result == [2, 4, 6]
    # Mapping over a tuple of strings
    result = map_structure(str.upper, ("a", "b", "c"))
    assert result == ("A", "B", "C")
    # Mapping over a set of booleans
    result = map_structure(int, {True, False})
    assert result == {1, 0}

def test_map_structure_nested_collections():
    # Nested structures with dicts, lists, tuples, and sets
    nested = {
        "numbers": [1, 2, 3],
        "letters": ("a", "b"),
        "flags": {True, False},
        "inner": {"x": 10, "y": 20}
    }
    result = map_structure(lambda x: x + 1 if isinstance(x, int) else x, nested)
    assert result == {
        "numbers": [2, 3, 4],
        "letters": ("a", "b"),
        "flags": {1, 0},
        "inner": {"x": 11, "y": 21}
    }

def test_map_structure_error_propagation():
    # Function that raises an exception for a specific value
    def raise_on_three(x):
        if x == 3:
            raise ValueError("Three is not allowed")
        return x
    with pytest.raises(ValueError, match="Three is not allowed"):
        map_structure(raise_on_three, [1, 2, 3, 4])
