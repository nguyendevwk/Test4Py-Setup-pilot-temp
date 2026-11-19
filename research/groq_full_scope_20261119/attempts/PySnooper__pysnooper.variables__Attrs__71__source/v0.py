import itertools
import pytest
from pysnooper.variables import Attrs

class SlotClass:
    __slots__ = ('a', 'b')
    def __init__(self):
        self.a = 1
        self.b = 2

class DictClass:
    def __init__(self):
        self.x = 10
        self.y = 20

def test_keys_with_dict_and_slots():
    obj = SlotClass()
    obj.__dict__['extra'] = 'value'
    attrs = Attrs()
    keys = list(attrs._keys(obj))
    # Should contain dict keys and slot names
    assert 'extra' in keys
    assert 'a' in keys
    assert 'b' in keys
    # No duplicates
    assert len(keys) == len(set(keys))

def test_format_key():
    attrs = Attrs()
    assert attrs._format_key('foo') == '.foo'
    assert attrs._format_key('bar') == '.bar'

def test_get_value_error():
    obj = DictClass()
    attrs = Attrs()
    # Existing attribute
    assert attrs._get_value(obj, 'x') == 10
    # Non‑existent attribute should raise AttributeError
    with pytest.raises(AttributeError):
        attrs._get_value(obj, 'nonexistent')
