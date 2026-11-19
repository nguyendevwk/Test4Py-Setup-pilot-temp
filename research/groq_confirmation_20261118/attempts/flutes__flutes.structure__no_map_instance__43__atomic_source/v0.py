import pytest
from flutes.structure import no_map_instance

# Helper attribute name used by the implementation
_NO_MAP_INSTANCE_ATTR = "_NO_MAP_INSTANCE_ATTR"

def test_no_map_instance_sets_attribute_on_mutable_object():
    class Mutable:
        pass

    obj = Mutable()
    result = no_map_instance(obj)
    # The function should return the same instance
    assert result is obj
    # The attribute should be set to True
    assert getattr(result, _NO_MAP_INSTANCE_ATTR) is True

def test_no_map_instance_fallback_for_immutable_builtin():
    # Built-in types like int cannot have attributes set
    original = 42
    result = no_map_instance(original)
    # The result should not be the same object
    assert result is not original
    # The result should have the marker attribute set to True
    assert getattr(result, _NO_MAP_INSTANCE_ATTR) is True
    # The original value should remain unchanged
    assert original == 42

def test_no_map_instance_returns_same_for_custom_object_with_setattr():
    class Custom:
        def __init__(self):
            self.existing = "value"

    custom_obj = Custom()
    result = no_map_instance(custom_obj)
    # Should return the same instance
    assert result is custom_obj
    # Existing attribute remains intact
    assert result.existing == "value"
    # Marker attribute is set
    assert getattr(result, _NO_MAP_INSTANCE_ATTR) is True
