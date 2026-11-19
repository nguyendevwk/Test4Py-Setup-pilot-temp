import itertools
import pytest
from pysnooper.variables import Attrs

class SimpleDictObj:
    def __init__(self):
        self.__dict__ = {'a': 1, 'b': 2}

class SimpleSlotsObj:
    __slots__ = ('x', 'y')
    def __init__(self):
        self.x = 10
        self.y = 20

class MixedObj:
    __slots__ = ('s',)
    def __init__(self):
        self.__dict__ = {'d': 3}
        self.s = 4

def test_attrs_keys_combines_dict_and_slots():
    obj = MixedObj()
    attrs = Attrs()
    keys = list(attrs._keys(obj))
    # Should contain both dict keys and slot names
    assert set(keys) == {'d', 's'}
    # Order: dict keys first, then slots
    assert keys[0] == 'd' and keys[1] == 's'

def test_attrs_format_and_get_value_success():
    obj = SimpleSlotsObj()
    attrs = Attrs()
    # Format key should prepend a dot
    formatted = attrs._format_key('x')
    assert formatted == '.x'
    # Get value should return the attribute value
    value = attrs._get_value(obj, 'x')
    assert value == 10
    # Ensure that accessing a dict attribute works as well
    dict_obj = SimpleDictObj()
    value_dict = attrs._get_value(dict_obj, 'a')
    assert value_dict == 1

def test_attrs_get_value_missing_attribute_raises():
    obj = SimpleDictObj()
    attrs = Attrs()
    with pytest.raises(AttributeError):
        attrs._get_value(obj, 'nonexistent')
