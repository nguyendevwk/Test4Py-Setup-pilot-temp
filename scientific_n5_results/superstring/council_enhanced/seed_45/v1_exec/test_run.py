import pytest
from superstring.superstring import SuperString

def test_superstring_length_caching():
    content = "Hello, World!"
    s = SuperString(content)

    # _length should not exist before first call
    assert not hasattr(s, "_length")

    # First call computes and caches length
    first_len = s.length()
    assert isinstance(first_len, int)
    assert first_len == len(content)
    assert hasattr(s, "_length")
    assert s._length == first_len

    # Subsequent call returns cached value without recomputing
    second_len = s.length()
    assert second_len == first_len
    assert s._length == first_len
