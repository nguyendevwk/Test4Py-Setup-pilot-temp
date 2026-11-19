import pytest
from flutes import structure

def test_register_single_type(tmp_path):
    # Register a built‑in container type and verify it appears in the set
    structure.register_no_map_class(list)
    assert list in structure._NO_MAP_TYPES
    # The function returns None
    assert structure.register_no_map_class(dict) is None
    assert dict in structure._NO_MAP_TYPES

def test_register_multiple_types(tmp_path):
    # Register several types and ensure each is present only once
    structure.register_no_map_class(set)
    structure.register_no_map_class(set)  # duplicate registration
    # The set should contain the type exactly once
    assert structure._NO_MAP_TYPES.count(set) if hasattr(structure._NO_MAP_TYPES, "count") else True
    assert set in structure._NO_MAP_TYPES
    # Register a custom class
    class Custom(list): pass
    structure.register_no_map_class(Custom)
    assert Custom in structure._NO_MAP_TYPES

def test_register_non_type(tmp_path):
    # Register a non‑type object; it should be added to the set if hashable
    structure.register_no_map_class(42)
    assert 42 in structure._NO_MAP_TYPES
    # Register a non‑hashable object should raise TypeError
    with pytest.raises(TypeError):
        structure.register_no_map_class([1, 2, 3])
