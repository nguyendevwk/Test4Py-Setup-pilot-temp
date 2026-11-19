import pytest
from flutes.structure import no_map_instance

# The attribute name used internally by no_map_instance
_NO_MAP_INSTANCE_ATTR = "_NO_MAP_INSTANCE_ATTR"

def test_no_map_instance_sets_attribute_on_mutable():
    """When the instance allows attribute setting, the attribute is added."""
    lst = [1, 2, 3]
    result = no_map_instance(lst)
    # The function should return the same object
    assert result is lst
    # The marker attribute should be present and truthy
    assert getattr(result, _NO_MAP_INSTANCE_ATTR, False) is True

def test_no_map_instance_returns_same_type_for_immutable():
    """When the instance does not allow attribute setting, a new instance of the same type is returned."""
    num = 42
    result = no_map_instance(num)
    # The result should be an int (same type)
    assert isinstance(result, int)
    # For immutable built‑ins like int, the result is the same object
    assert result is num
    # The marker attribute should not exist on immutable types
    assert not hasattr(result, _NO_MAP_INSTANCE_ATTR)

def test_no_map_instance_on_custom_slots_class():
    """Instances of classes with __slots__ that do not allow arbitrary attributes should be handled correctly."""
    class SlotClass:
        __slots__ = ("value",)

        def __init__(self, value):
            self.value = value

    obj = SlotClass(10)
    result = no_map_instance(obj)
    # The result should be the same object
    assert result is obj
    # Since __slots__ does not include the marker, setting it should raise AttributeError
    # and the function should return a new instance via _no_map_type
    # We check that the returned object is still an instance of SlotClass
    assert isinstance(result, SlotClass)
    # The marker attribute should not be present
    assert not hasattr(result, _NO_MAP_INSTANCE_ATTR)
