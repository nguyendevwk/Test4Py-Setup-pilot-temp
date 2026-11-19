import pytest
from tornado.escape import recursive_unicode

def test_recursive_unicode_converts_bytes_and_nested_structures():
    # Input contains nested dict, list, tuple and byte strings
    data = {
        b'key1': b'value1',
        'key2': [b'list_item1', {'inner_key': b'inner_value'}],
        'key3': (b'tuple_item1', b'tuple_item2')
    }
    result = recursive_unicode(data)
    # All byte strings should be converted to str (unicode in Python3)
    assert isinstance(result, dict)
    assert result['key1'] == 'value1'
    assert result['key2'] == ['list_item1', {'inner_key': 'inner_value'}]
    assert result['key3'] == ('tuple_item1', 'tuple_item2')
    # Original keys that were bytes should also be converted
    assert b'key1' not in result
    assert 'key1' in result

def test_recursive_unicode_handles_empty_collections():
    # Empty structures should be returned unchanged but still of the same type
    empty_dict = {}
    empty_list = []
    empty_tuple = ()
    assert recursive_unicode(empty_dict) == {}
    assert recursive_unicode(empty_list) == []
    assert recursive_unicode(empty_tuple) == ()

def test_recursive_unicode_returns_non_bytes_unmodified():
    # Objects that are not bytes, dict, list, or tuple should be returned unchanged
    class CustomObj:
        pass
    obj = CustomObj()
    result = recursive_unicode(obj)
    assert result is obj
    # Also test that a string is returned unchanged
    s = "already unicode"
    assert recursive_unicode(s) is s
