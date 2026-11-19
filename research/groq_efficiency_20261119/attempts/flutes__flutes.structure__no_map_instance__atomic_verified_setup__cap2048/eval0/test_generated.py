import pytest
from flutes.structure import no_map_instance, _NO_MAP_INSTANCE_ATTR

def test_no_map_instance_sets_attribute_on_mutable():
    lst = [1, 2, 3]
    result = no_map_instance(lst)
    assert result is lst
    assert hasattr(result, _NO_MAP_INSTANCE_ATTR)
    assert getattr(result, _NO_MAP_INSTANCE_ATTR) is True

def test_no_map_instance_returns_same_for_immutable():
    num = 42
    result = no_map_instance(num)
    # For immutable types, a new wrapper is returned, not the original int
    assert result is not num
    # The wrapper should not be an instance of int
    assert not isinstance(result, int)
    # The wrapper should still be truthy and equal to the original value
    assert result == num

def test_no_map_instance_is_idempotent():
    d = {"a": 1}
    first = no_map_instance(d)
    second = no_map_instance(first)
    assert first is second
    assert hasattr(first, _NO_MAP_INSTANCE_ATTR)
    assert getattr(first, _NO_MAP_INSTANCE_ATTR) is True
