import pytest
from flutes.structure import no_map_instance

# Helper attribute name used by the implementation
_NO_MAP_INSTANCE_ATTR = "_NO_MAP_INSTANCE_ATTR"

def test_no_map_instance_sets_attribute_on_mutable():
    """For mutable objects (e.g., list) the function should set the marker attribute."""
    lst = [1, 2, 3]
    result = no_map_instance(lst)
    # The function should return the same instance
    assert result is lst
    # The marker attribute should be present and truthy
    assert getattr(result, _NO_MAP_INSTANCE_ATTR, False) is True
    # Calling again should not change the attribute value
    second = no_map_instance(lst)
    assert second is lst
    assert getattr(second, _NO_MAP_INSTANCE_ATTR, False) is True

def test_no_map_instance_returns_same_for_immutable():
    """For immutable objects (e.g., int) the function should return an instance of the same type."""
    num = 42
    result = no_map_instance(num)
    # The returned object should be of the same type
    assert isinstance(result, type(num))
    # Since integers cannot have arbitrary attributes, the marker should not be set
    assert not hasattr(result, _NO_MAP_INSTANCE_ATTR)

def test_no_map_instance_on_custom_class_without_setattr():
    """If the instance's class does not allow setting attributes, the fallback should still return an instance."""
    class NoSetAttr:
        __slots__ = ()
    obj = NoSetAttr()
    result = no_map_instance(obj)
    # The returned object should be an instance of the same type
    assert isinstance(result, type(obj))
    # The marker attribute should not be present because __slots__ prevents it
    assert not hasattr(result, _NO_MAP_INSTANCE_ATTR)
