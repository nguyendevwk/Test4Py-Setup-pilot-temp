import pytest
from pysnooper.variables import Keys

def test_keys_extraction_and_access(tmp_path):
    # Create a sample dictionary with various key types
    sample = {
        'alpha': 1,
        42: 'answer',
        (1, 2): [3, 4],
        'beta': {'nested': True}
    }
    keys_obj = Keys()
    # _keys should return the dict's keys view
    keys_view = keys_obj._keys(sample)
    assert isinstance(keys_view, dict_keys)
    assert set(keys_view) == set(sample.keys())

    # _get_value should retrieve the correct values
    for key in sample:
        assert keys_obj._get_value(sample, key) == sample[key]

def test_format_key_representation(tmp_path):
    keys_obj = Keys()
    # Test formatting for different key types
    assert keys_obj._format_key('simple') == '[simple]'
    assert keys_obj._format_key(123) == '[123]'
    assert keys_obj._format_key((1, 2)) == '[(1, 2)]'
    # Ensure that the representation is shortish (no long repr)
    long_key = 'x' * 100
    formatted = keys_obj._format_key(long_key)
    assert formatted.startswith('[')
    assert formatted.endswith(']')
    # The representation should be truncated if too long
    assert len(formatted) < len(long_key) + 2

def test_error_on_missing_key(tmp_path):
    keys_obj = Keys()
    sample = {'exists': 42}
    # Accessing a non-existent key should raise KeyError
    with pytest.raises(KeyError):
        keys_obj._get_value(sample, 'missing')
