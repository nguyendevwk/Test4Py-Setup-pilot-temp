import itertools
import pytest
from pysnooper.variables import Attrs

class DummyWithDict:
    def __init__(self):
        self.x = 10
        self.y = 20

class DummyWithSlots:
    __slots__ = ('a', 'b')
    def __init__(self):
        self.a = 'foo'
        self.b = 'bar'

class DummyBoth:
    __slots__ = ('s',)
    def __init__(self):
        self.s = 1
        self.t = 2

def test_keys_collects_dict_and_slots():
    attrs = Attrs()
    dummy = DummyBoth()
    keys = list(attrs._keys(dummy))
    # __dict__ contains 't', __slots__ contains 's'
    assert 't' in keys
    assert 's' in keys
    # No duplicate keys
    assert len(keys) == 2

def test_format_key_prefixes_with_dot():
    attrs = Attrs()
    assert attrs._format_key('foo') == '.foo'
    assert attrs._format_key('bar') == '.bar'

def test_get_value_raises_for_missing_attribute():
    attrs = Attrs()
    dummy = DummyWithDict()
    with pytest.raises(AttributeError):
        attrs._get_value(dummy, 'nonexistent')
