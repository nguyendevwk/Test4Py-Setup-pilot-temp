import pytest
from flutes.structure import map_structure


def test_map_structure_over_list():
    """Map a simple function over a flat list."""
    result = map_structure(lambda x: x * 2, [1, 2, 3])
    assert result == [2, 4, 6]
    # Ensure the original list is not mutated
    assert [1, 2, 3] == [1, 2, 3]


def test_map_structure_nested_collections():
    """Map over a nested structure containing dicts, lists, tuples, and sets."""
    nested = {
        "numbers": [1, 2, 3],
        "letters": ("a", "b"),
        "unique": {4, 5},
    }
    result = map_structure(str, nested)
    assert isinstance(result, dict)
    assert result["numbers"] == ["1", "2", "3"]
    assert result["letters"] == ("a", "b")  # strings unchanged
    assert result["unique"] == {"4", "5"}
    # Original structure remains unchanged
    assert nested["numbers"] == [1, 2, 3]
    assert nested["letters"] == ("a", "b")
    assert nested["unique"] == {4, 5}


def test_map_structure_non_collection_and_error():
    """Passing a non‑collection should apply the function directly, and
    exceptions from the function should propagate."""
    # Non‑collection: an integer
    assert map_structure(lambda x: x + 10, 5) == 15

    # Function that raises an exception
    def bad_fn(x):
        raise ValueError("bad value")

    with pytest.raises(ValueError, match="bad value"):
        map_structure(bad_fn, [1, 2, 3])
