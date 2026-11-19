import pytest
from flutes.structure import no_map_instance

class Dummy:
    """Simple mutable object for testing."""
    def __init__(self, value):
        self.value = value

def test_no_map_instance_sets_attribute_and_returns_same_object():
    """Calling no_map_instance on a mutable object should set the marker attribute
    and return the same object."""
    obj = Dummy(10)
    result = no_map_instance(obj)
    # The function should return the same instance
    assert result is obj
    # The marker attribute should be present and truthy
    assert getattr(obj, "_NO_MAP_INSTANCE_ATTR", False) is True

def test_no_map_instance_is_idempotent():
    """Calling no_map_instance twice on the same object should not alter the
    object or create a new instance."""
    obj = Dummy(20)
    first = no_map_instance(obj)
    second = no_map_instance(first)
    assert first is second
    assert getattr(obj, "_NO_MAP_INSTANCE_ATTR", False) is True

def test_no_map_instance_on_immutable_type_returns_wrapper():
    """For immutable built‑in types (e.g., int) the function should return a
    wrapper instance that is not the original object."""
    original = 42
    wrapped = no_map_instance(original)
    # The wrapped object should not be the same as the original int
    assert wrapped is not original
    # The wrapped object should still be truthy and not raise AttributeError
    # when accessing the marker attribute
    assert getattr(wrapped, "_NO_MAP_INSTANCE_ATTR", False) is True
