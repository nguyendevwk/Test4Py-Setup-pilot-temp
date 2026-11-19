import pytest
from superstring.superstring import SuperString

def test_superstring_length_caching():
    """Length should be computed once and cached in _length."""
    s = SuperString("hello")
    # Before calling length, _length should not exist
    assert not hasattr(s, "_length")
    # First call computes and caches the length
    first = s.length()
    assert first == 5
    assert hasattr(s, "_length") and s._length == 5
    # Subsequent calls return the cached value
    second = s.length()
    assert second == 5
    assert s._length == 5
