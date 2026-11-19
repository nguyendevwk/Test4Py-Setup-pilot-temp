import pytest
from flutes.structure import no_map_instance

# Helper attribute name used by the function (should match the internal constant)
_NO_MAP_INSTANCE_ATTR = "_NO_MAP_INSTANCE_ATTR"

def test_no_map_instance_sets_attribute_on_mutable_object():
    """When the instance is mutable, the function should set the marker attribute."""
    class MutableContainer:
        def __init__(self, data):
            self.data = data

    container = MutableContainer([1, 2, 3])
    result = no_map_instance(container)

    # The function should return the same object
    assert result is container
    # The marker attribute should be present and truthy
    assert hasattr(result, _NO_MAP_INSTANCE_ATTR)
    assert getattr(result, _NO_MAP_INSTANCE_ATTR) is True

def test_no_map_instance_returns_same_object_for_immutable():
    """When the instance is immutable, the function should return an instance of the same type."""
    immutable_value = 42
    result = no_map_instance(immutable_value)

    # The returned value should be equal to the original
    assert result == immutable_value
    # It should be the same type
    assert type(result) is type(immutable_value)
    # Since integers are immutable, the returned object should be the same object
    assert result is immutable_value

def test_no_map_instance_fallback_for_non_settable_object():
    """If setattr fails, the function should use the fallback mechanism and still return a valid instance."""
    class ReadOnly:
        __slots__ = ("value",)

        def __init__(self, value):
            self.value = value

    ro = ReadOnly("test")
    result = no_map_instance(ro)

    # The returned object should be equal to the original
    assert result == ro
    # It should be the same type
    assert type(result) is type(ro)
    # The marker attribute should not be set on the original (since __slots__ prevents it)
    assert not hasattr(ro, _NO_MAP_INSTANCE_ATTR)
    # The returned object should have the marker attribute
    assert hasattr(result, _NO_MAP_INSTANCE_ATTR)
    assert getattr(result, _NO_MAP_INSTANCE_ATTR) is True
