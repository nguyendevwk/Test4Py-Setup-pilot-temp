import pytest
from superstring.superstring import SuperString

def test_superstring_length_caching():
    content = "abc"
    s = SuperString(content)

    # First call computes and caches the length
    first_len = s.length()
    assert first_len == len(content)
    assert hasattr(s, "_length")
    assert s._length == len(content)

    # Subsequent call should return the cached value unchanged
    second_len = s.length()
    assert second_len == first_len
    assert s._length == len(content)
