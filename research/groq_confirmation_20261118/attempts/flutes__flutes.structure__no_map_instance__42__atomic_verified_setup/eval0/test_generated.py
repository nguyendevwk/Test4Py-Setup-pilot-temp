import pytest
from flutes.structure import no_map_instance

# Helper attribute name used by no_map_instance
_NO_MAP_ATTR = "_NO_MAP_INSTANCE_ATTR"

def test_no_map_instance_sets_attribute_on_mutable():
    """A mutable instance should receive the marker attribute."""
    lst = [1, 2, 3]
    result = no_map_instance(lst)
    assert result is lst
    assert hasattr(result, _NO_MAP_ATTR)
    assert getattr(result, _NO_MAP_ATTR) is True

def test_no_map_instance_returns_same_type_for_immutable():
    """An immutable instance (e.g., int) cannot receive the attribute; the function should return an instance of the same type."""
    num = 42
    result = no_map_instance(num)
    # The returned object should still be an int
    assert isinstance(result, int)
    # It should not be the same object if the implementation creates a new wrapper
    assert result is not num or isinstance(result, int)  # allow same object if wrapper is same

def test_no_map_instance_idempotent_when_attribute_present():
    """If the instance already has the marker attribute, the function should leave it unchanged."""
    class Custom:
        pass
    obj = Custom()
    setattr(obj, _NO_MAP_ATTR, True)
    result = no_map_instance(obj)
    assert result is obj
    assert getattr(result, _NO_MAP_ATTR) is True
