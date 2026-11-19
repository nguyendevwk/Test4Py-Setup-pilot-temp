import pytest
from tornado.escape import recursive_unicode, to_unicode

def test_recursive_unicode_converts_bytes_in_dict_and_list():
    data = {
        b'key1': b'value1',
        'key2': [b'item1', b'item2', {'nested': b'bytes'}],
        'key3': (b'tuple_item',)
    }
    result = recursive_unicode(data)
    assert isinstance(result, dict)
    assert result['key1'] == 'value1'
    assert result['key2'] == ['item1', 'item2', {'nested': 'bytes'}]
    assert result['key3'] == ('tuple_item',)

def test_recursive_unicode_preserves_non_bytes_and_non_iterables():
    data = [b'bytes', 123, None, True, 3.14]
    result = recursive_unicode(data)
    assert result == ['bytes', 123, None, True, 3.14]
    # Ensure original list is unchanged
    assert data[0] == b'bytes'

def test_recursive_unicode_handles_empty_and_nested_structures():
    data = {'empty_list': [], 'empty_dict': {}, 'empty_tuple': ()}
    result = recursive_unicode(data)
    assert result == {'empty_list': [], 'empty_dict': {}, 'empty_tuple': ()}
    # Nested empty structures should remain empty and of same type
    assert isinstance(result['empty_list'], list)
    assert isinstance(result['empty_dict'], dict)
    assert isinstance(result['empty_tuple'], tuple)
