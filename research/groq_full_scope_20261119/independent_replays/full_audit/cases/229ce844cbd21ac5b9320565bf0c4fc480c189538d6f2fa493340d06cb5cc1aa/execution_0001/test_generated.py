import pytest
from flutes.structure import register_no_map_class, _NO_MAP_TYPES


def test_register_builtin_type():
    """Registering a built‑in container type should add it to the global set."""
    # Ensure the set is initially empty for this test
    _NO_MAP_TYPES.clear()
    register_no_map_class(list)
    assert list in _NO_MAP_TYPES
    # The set should contain exactly one element
    assert len(_NO_MAP_TYPES) == 1


def test_register_custom_class():
    """Registering a user‑defined class should also be tracked."""
    _NO_MAP_TYPES.clear()

    class CustomContainer:
        pass

    register_no_map_class(CustomContainer)
    assert CustomContainer in _NO_MAP_TYPES
    assert len(_NO_MAP_TYPES) == 1


def test_register_duplicate_no_effect():
    """Registering the same type twice should not duplicate entries."""
    _NO_MAP_TYPES.clear()
    register_no_map_class(dict)
    register_no_map_class(dict)
    # The set should still contain only one instance of dict
    assert dict in _NO_MAP_TYPES
    assert len(_NO_MAP_TYPES) == 1
