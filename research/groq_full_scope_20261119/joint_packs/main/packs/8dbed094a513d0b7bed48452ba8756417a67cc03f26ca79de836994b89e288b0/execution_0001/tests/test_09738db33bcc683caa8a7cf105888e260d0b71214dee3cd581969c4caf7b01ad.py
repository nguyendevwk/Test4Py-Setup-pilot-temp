import pytest
from flutes.structure import no_map_instance, _NO_MAP_INSTANCE_ATTR

# Test 1: Instance of a user-defined class can be marked directly
class CustomContainer:
    def __init__(self, data):
        self.data = data

def test_no_map_instance_sets_attribute_on_custom_object():
    obj = CustomContainer([1, 2, 3])
    result = no_map_instance(obj)
    assert result is obj
    assert getattr(result, _NO_MAP_INSTANCE_ATTR) is True
    # Ensure the original object is unchanged except for the new attribute
    assert result.data == [1, 2, 3]

# Test 2: Built-in mutable container (list) is wrapped in a subclass
def test_no_map_instance_wraps_builtin_list():
    lst = [4, 5, 6]
    wrapped = no_map_instance(lst)
    # The returned object should be a different instance (subclass)
    assert wrapped is not lst
    assert isinstance(wrapped, list)
    assert getattr(wrapped, _NO_MAP_INSTANCE_ATTR) is True
    # The contents should be preserved
    assert wrapped == [4, 5, 6]

# Test 3: Attempting to set attribute on an immutable built-in raises AttributeError
# and the function falls back to creating a subclass (which works for tuples)
def test_no_map_instance_fallback_for_tuple():
    tpl = (7, 8, 9)
    wrapped = no_map_instance(tpl)
    # The returned object should be a different instance (subclass)
    assert wrapped is not tpl
    assert isinstance(wrapped, tuple)
    assert getattr(wrapped, _NO_MAP_INSTANCE_ATTR) is True
    assert wrapped == (7, 8, 9)
