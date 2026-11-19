import pytest
from superstring.superstring import SuperString

def test_superstring_length_caching():
    content = "hello world"
    ss = SuperString(content)

    # Length should not be cached before first call
    assert not hasattr(ss, "_length")

    # First call computes and caches the length
    first_len = ss.length()
    assert first_len == len(content)
    assert hasattr(ss, "_length")
    assert ss._length == len(content)

    # Subsequent call returns the cached value
    second_len = ss.length()
    assert second_len == first_len
    assert ss._length == first_len
