import pytest
from flutes import structure

def test_register_new_type_adds_to_set():
    # Ensure that a new type is added to the internal set
    initial_len = len(structure._NO_MAP_TYPES)
    structure.register_no_map_class(set)
    assert set in structure._NO_MAP_TYPES
    assert len(structure._NO_MAP_TYPES) == initial_len + 1

def test_register_same_type_idempotent():
    # Registering the same type twice should not increase the set size
    structure.register_no_map_class(dict)
    first_len = len(structure._NO_MAP_TYPES)
    structure.register_no_map_class(dict)
    assert len(structure._NO_MAP_TYPES) == first_len

def test_register_multiple_types_and_membership():
    # Register multiple types and verify membership and non-membership
    structure.register_no_map_class(list)
    structure.register_no_map_class(tuple)
    assert list in structure._NO_MAP_TYPES
    assert tuple in structure._NO_MAP_TYPES
    assert int not in structure._NO_MAP_TYPES
