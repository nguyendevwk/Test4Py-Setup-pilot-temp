import pytest
from flutes.structure import no_map_instance

class Dummy:
    pass

def test_no_map_instance_sets_attribute_on_mutable_object():
    obj = Dummy()
    result = no_map_instance(obj)
    # The function should return the same instance
    assert result is obj
    # The special attribute should be set to True
    assert getattr(result, "_NO_MAP_INSTANCE_ATTR", None) is True

def test_no_map_instance_returns_new_object_for_immutable_type():
    original = (1, 2, 3)
    result = no_map_instance(original)
    # The returned object should not be the same as the original tuple
    assert result is not original
    # It should still be a tuple (or a subclass) containing the same elements
    assert isinstance(result, tuple)
    assert tuple(result) == original
    # The special attribute should be present on the new object
    assert getattr(result, "_NO_MAP_INSTANCE_ATTR", None) is True

def test_no_map_instance_attribute_persistence_on_subsequent_calls():
    obj = Dummy()
    first = no_map_instance(obj)
    # Calling again should not change the attribute value
    second = no_map_instance(first)
    assert second is first
    assert getattr(second, "_NO_MAP_INSTANCE_ATTR") is True
