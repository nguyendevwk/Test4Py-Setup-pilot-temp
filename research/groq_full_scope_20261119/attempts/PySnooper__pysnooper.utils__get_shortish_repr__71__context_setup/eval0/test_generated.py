import pytest
from pysnooper.utils import get_shortish_repr, get_repr_function, normalize_repr, truncate

def test_get_shortish_repr_basic_and_truncate():
    # Basic representation of an integer
    assert get_shortish_repr(42) == '42'
    # Truncate a long string
    long_str = 'abcdefghijklmnopqrstuvwxyz'
    truncated = get_shortish_repr(long_str, max_length=10)
    # Should contain first 4 chars, ellipsis, last 3 chars
    assert truncated == 'abcd...xyz'
    # Ensure length does not exceed max_length
    assert len(truncated) == 10

def test_get_shortish_repr_custom_repr_and_normalize():
    # Custom representation for list types
    custom = [(list, lambda x: f'List({len(x)})')]
    assert get_shortish_repr([1, 2, 3], custom_repr=custom) == 'List(3)'
    # Normalize removes memory addresses from default repr
    class Dummy:
        def __repr__(self):
            return f'<Dummy at 0x1234>'
    dummy = Dummy()
    normalized = get_shortish_repr(dummy, normalize=True)
    assert normalized == '<Dummy>'
    # Ensure normalize does not alter string without addresses
    assert get_shortish_repr('plain string', normalize=True) == 'plain string'

def test_get_repr_function_and_truncate_edge_cases():
    # get_repr_function should return repr for unknown types
    assert get_repr_function('test', ()) is repr
    # Custom repr for a specific instance
    custom = [(lambda x: isinstance(x, str) and x.startswith('a'), lambda x: 'alpha')]
    assert get_repr_function('apple', custom)('apple') == 'alpha'
    # truncate with max_length equal to string length
    s = 'short'
    assert truncate(s, len(s)) == s
    # truncate with max_length less than string length
    assert truncate('123456', 4) == '1...6'
