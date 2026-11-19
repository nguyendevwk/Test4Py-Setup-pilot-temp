import pytest
from flutes.structure import register_no_map_class, _NO_MAP_TYPES


def test_register_single_type_adds_to_set():
    """Registering a built‑in container type adds it to the internal set."""
    # Ensure the set is initially empty for this test
    _NO_MAP_TYPES.clear()
    register_no_map_class(list)
    assert list in _NO_MAP_TYPES, "list should be registered as a non‑mappable type"


def test_register_subclass_is_treated_separately():
    """Registering a subclass of a container type registers the subclass, not the base."""
    _NO_MAP_TYPES.clear()

    class MyList(list):
        pass

    register_no_map_class(MyList)
    assert MyList in _NO_MAP_TYPES, "subclass MyList should be registered"
    assert list not in _NO_MAP_TYPES, "base list should not be automatically registered"


def test_registering_same_type_twice_does_not_duplicate():
    """Registering the same type twice does not increase the set size."""
    _NO_MAP_TYPES.clear()
    register_no_map_class(dict)
    size_after_first = len(_NO_MAP_TYPES)
    register_no_map_class(dict)
    size_after_second = len(_NO_MAP_TYPES)
    assert size_after_first == size_after_second == 1, (
        "Registering the same type twice should not duplicate entries"
    )
