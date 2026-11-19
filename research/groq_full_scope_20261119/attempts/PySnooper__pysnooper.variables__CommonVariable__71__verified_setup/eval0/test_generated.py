import pytest
from pysnooper.variables import CommonVariable
from pysnooper import utils

class DummyVariable(CommonVariable):
    """Concrete implementation of CommonVariable for testing."""
    def __init__(self, source, unambiguous_source, exclude=None):
        super().__init__(source, unambiguous_source, exclude or set())

    def _keys(self, main_value):
        # Return all keys of a dict
        return main_value.keys()

    def _format_key(self, key):
        # Simple formatting: wrap key in brackets
        return f'[{key}]'

    def _get_value(self, main_value, key):
        # Return the value; raise if key is 'error'
        if key == 'error':
            raise ValueError("Intentional error")
        return main_value[key]

def test_normal_behavior():
    """Test that _items returns correct representations for a normal dict."""
    data = {'a': 1, 'b': 2}
    var = DummyVariable('src', 'src_')
    items = var._items(data)
    # First item is the source representation
    assert items[0] == ('src', utils.get_shortish_repr(data))
    # Subsequent items correspond to keys 'a' and 'b'
    expected = [
        ('src_[a]', utils.get_shortish_repr(1)),
        ('src_[b]', utils.get_shortish_repr(2)),
    ]
    assert items[1:] == expected

def test_exclude_key():
    """Test that keys in the exclude set are omitted."""
    data = {'a': 1, 'b': 2}
    var = DummyVariable('src', 'src_', exclude={'b'})
    items = var._items(data)
    # Only key 'a' should appear
    assert len(items) == 2
    assert items[1] == ('src_[a]', utils.get_shortish_repr(1))
    assert all('b' not in key for key, _ in items)

def test_error_in_get_value():
    """Test that a key raising an exception is skipped."""
    data = {'a': 1, 'error': 3}
    var = DummyVariable('src', 'src_')
    items = var._items(data)
    # 'error' key should be omitted due to exception
    keys = [k for k, _ in items]
    assert 'src_[error]' not in keys
    # Ensure other keys are present
    assert 'src_[a]' in keys
