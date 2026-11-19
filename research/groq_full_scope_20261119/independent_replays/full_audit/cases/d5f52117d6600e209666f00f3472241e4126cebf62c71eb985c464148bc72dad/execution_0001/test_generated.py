import pytest
from flutes.structure import register_no_map_class, _NO_MAP_TYPES

def test_register_single_type():
    """Registering a new type adds it to the internal set."""
    # Ensure the type is not already registered
    assert int not in _NO_MAP_TYPES
    register_no_map_class(int)
    assert int in _NO_MAP_TYPES

def test_register_same_type_idempotent():
    """Registering the same type multiple times does not duplicate entries."""
    _NO_MAP_TYPES.discard(str)  # clean state
    register_no_map_class(str)
    register_no_map_class(str)
    # The set should contain the type only once
    assert list(_NO_MAP_TYPES).count(str) == 1

def test_register_different_types():
    """Registering different types affects only those types."""
    _NO_MAP_TYPES.discard(list)
    _NO_MAP_TYPES.discard(dict)
    register_no_map_class(list)
    assert list in _NO_MAP_TYPES
    assert dict not in _NO_MAP_TYPES
