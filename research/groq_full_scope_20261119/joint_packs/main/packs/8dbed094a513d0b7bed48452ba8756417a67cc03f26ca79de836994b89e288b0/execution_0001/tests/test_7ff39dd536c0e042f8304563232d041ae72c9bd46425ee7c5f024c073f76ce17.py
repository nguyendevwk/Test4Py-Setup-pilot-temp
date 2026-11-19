import pytest
from flutes.structure import register_no_map_class, _NO_MAP_TYPES

def test_register_new_type_adds_to_set():
    """Registering a new type should add it to the global set."""
    # Ensure the set is initially empty for this test
    _NO_MAP_TYPES.clear()
    register_no_map_class(list)
    assert list in _NO_MAP_TYPES, "list should be registered as non-mappable"

def test_register_same_type_idempotent():
    """Registering the same type twice should not duplicate entries."""
    _NO_MAP_TYPES.clear()
    register_no_map_class(dict)
    register_no_map_class(dict)
    # Set should contain exactly one instance of dict
    assert list(_NO_MAP_TYPES) == [dict], "duplicate registration should not add multiple entries"

def test_register_subclass_is_stored_independently():
    """Registering a subclass should store the subclass separately from its base."""
    _NO_MAP_TYPES.clear()
    class CustomList(list): pass
    register_no_map_class(CustomList)
    assert CustomList in _NO_MAP_TYPES, "CustomList should be registered"
    assert list not in _NO_MAP_TYPES, "Base list should not be implicitly registered"
