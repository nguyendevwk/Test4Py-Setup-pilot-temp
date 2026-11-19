import pytest
from flutes.structure import no_map_instance, _NO_MAP_INSTANCE_ATTR

class Dummy:
    pass

def test_no_map_instance_sets_attribute_on_custom_object():
    obj = Dummy()
    result = no_map_instance(obj)
    assert result is obj
    assert hasattr(result, _NO_MAP_INSTANCE_ATTR)
    assert getattr(result, _NO_MAP_INSTANCE_ATTR) is True

def test_no_map_instance_wraps_builtin_list():
    lst = [1, 2, 3]
    wrapped = no_map_instance(lst)
    assert wrapped is not lst
    assert isinstance(wrapped, list)
    assert hasattr(wrapped, _NO_MAP_INSTANCE_ATTR)
    assert getattr(wrapped, _NO_MAP_INSTANCE_ATTR) is True
    assert wrapped == lst

def test_no_map_instance_returns_new_instance_for_immutable_type():
    tpl = (1, 2, 3)
    wrapped = no_map_instance(tpl)
    assert wrapped is not tpl
    assert isinstance(wrapped, tuple)
    assert hasattr(wrapped, _NO_MAP_INSTANCE_ATTR)
    assert getattr(wrapped, _NO_MAP_INSTANCE_ATTR) is True
    assert wrapped == tpl
