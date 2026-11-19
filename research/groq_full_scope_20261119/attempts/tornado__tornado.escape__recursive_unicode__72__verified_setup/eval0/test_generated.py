import pytest
from tornado.escape import recursive_unicode

def test_recursive_unicode_basic():
    # Bytes should be decoded to str
    assert recursive_unicode(b'hello') == 'hello'
    # Non-bytes should be returned unchanged
    assert recursive_unicode(42) == 42
    assert recursive_unicode('text') == 'text'

def test_recursive_unicode_nested():
    data = {
        'a': b'bytes',
        'b': [b'list', {'c': b'nested'}],
        'd': (b'tuple', {'e': b'inner'}),
    }
    expected = {
        'a': 'bytes',
        'b': ['list', {'c': 'nested'}],
        'd': ('tuple', {'e': 'inner'}),
    }
    assert recursive_unicode(data) == expected

def test_recursive_unicode_boundary():
    # Empty structures should be preserved
    assert recursive_unicode({}) == {}
    assert recursive_unicode([]) == []
    assert recursive_unicode(()) == ()
    # Mixed types with no bytes
    mixed = {'x': 1, 'y': [2, 3], 'z': (4, 5)}
    assert recursive_unicode(mixed) == mixed
