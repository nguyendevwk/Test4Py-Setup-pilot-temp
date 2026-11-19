import pytest
from flutes.structure import no_map_instance, _NO_MAP_INSTANCE_ATTR

class Dummy:
    pass

def test_no_map_instance_sets_attribute_on_mutable_object():
    obj = Dummy()
    result = no_map_instance(obj)
    # The function should return the same object
    assert result is obj
    # The attribute should be set to True
    assert getattr(obj, _NO_MAP_INSTANCE_ATTR) is True

def test_no_map_instance_on_immutable_type_returns_wrapper_with_attribute():
    # Using an immutable built-in type (int) which cannot have attributes set
    original = 42
    result = no_map_instance(original)
    # The result should not be the same object (since int is immutable)
    assert result is not original
    # The wrapper should have the marker attribute set to True
    assert getattr(result, _NO_MAP_INSTANCE_ATTR) is True
    # The original value should remain unchanged
    assert original == 42

def test_no_map_instance_on_non_settable_object_returns_wrapper_with_attribute():
    # Using a built-in type that does not allow arbitrary attribute assignment (e.g., tuple)
    original = (1, 2, 3)
    result = no_map_instance(original)
    # The result should not be the same object
    assert result is not original
    # The wrapper should have the marker attribute set to True
    assert getattr(result, _NO_MAP_INSTANCE_ATTR) is True
    # The original tuple should remain unchanged
    assert original == (1, 2, 3)
