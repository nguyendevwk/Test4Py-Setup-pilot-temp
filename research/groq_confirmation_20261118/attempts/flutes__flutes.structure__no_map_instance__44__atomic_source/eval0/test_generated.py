import pytest
from flutes.structure import no_map_instance, _NO_MAP_INSTANCE_ATTR, _no_map_type

class MutableContainer:
    def __init__(self, data):
        self.data = data

class ImmutableContainer(tuple):
    def __new__(cls, data):
        return super().__new__(cls, data)

def test_no_map_instance_sets_attribute_on_mutable():
    """Calling no_map_instance on a mutable object should set the marker attribute."""
    obj = MutableContainer([1, 2, 3])
    result = no_map_instance(obj)
    # The function should return the same object
    assert result is obj
    # The marker attribute must be present and truthy
    assert hasattr(result, _NO_MAP_INSTANCE_ATTR)
    assert getattr(result, _NO_MAP_INSTANCE_ATTR) is True

def test_no_map_instance_fallback_for_immutable():
    """If setting the attribute fails, the function should wrap the instance."""
    imm = ImmutableContainer([4, 5, 6])
    result = no_map_instance(imm)
    # The result should not be the original immutable instance
    assert result is not imm
    # The result should be an instance of the wrapper returned by _no_map_type
    wrapper_cls = _no_map_type(type(imm))
    assert isinstance(result, wrapper_cls)
    # The wrapper should expose the original data
    assert isinstance(result, tuple)
    assert result == imm
    # The marker attribute should be set on the wrapper
    assert hasattr(result, _NO_MAP_INSTANCE_ATTR)
    assert getattr(result, _NO_MAP_INSTANCE_ATTR) is True

def test_no_map_instance_attribute_error_on_builtin():
    """Built-in types that cannot have attributes should be wrapped."""
    # Use a built-in immutable type that cannot have attributes
    num = 42
    result = no_map_instance(num)
    # The result should be a wrapper instance, not the original int
    assert result is not num
    wrapper_cls = _no_map_type(type(num))
    assert isinstance(result, wrapper_cls)
    # The wrapper should preserve the value
    assert result == num
    # The marker attribute should be present on the wrapper
    assert hasattr(result, _NO_MAP_INSTANCE_ATTR)
    assert getattr(result, _NO_MAP_INSTANCE_ATTR) is True
