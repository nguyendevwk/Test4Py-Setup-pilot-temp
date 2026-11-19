import pytest
from tornado.escape import recursive_unicode, to_unicode

def test_recursive_unicode_converts_bytes_in_nested_structures():
    data = {
        b'key1': [b'value1', (b'value2',)],
        'key2': {'nested': b'value3'}
    }
    result = recursive_unicode(data)
    assert isinstance(result, dict)
    assert isinstance(result['key1'], list)
    assert isinstance(result['key1'][0], str)
    assert isinstance(result['key1'][1], tuple)
    assert isinstance(result['key1'][1][0], str)
    assert isinstance(result['key2']['nested'], str)
    assert result['key1'][0] == 'value1'
    assert result['key1'][1][0] == 'value2'
    assert result['key2']['nested'] == 'value3'

def test_recursive_unicode_handles_empty_and_non_byte_types():
    empty_list = []
    empty_dict = {}
    empty_tuple = ()
    mixed = [b'bytes', 123, None, 'unicode', empty_dict]
    result = recursive_unicode(mixed)
    assert result == ['bytes', 123, None, 'unicode', {}]
    assert recursive_unicode(empty_list) == []
    assert recursive_unicode(empty_dict) == {}
    assert recursive_unicode(empty_tuple) == ()

def test_recursive_unicode_raises_on_invalid_utf8_bytes():
    invalid_bytes = b'\xff\xfe\xfa'
    with pytest.raises(UnicodeDecodeError):
        recursive_unicode(invalid_bytes)
