import pytest
from superstring.superstring import SuperString

def test_superstring_length_caching():
    content = "Hello, World!"
    s = SuperString(content)

    # _length should not exist before first call
    assert "_length" not in s.__dict__

    # First call computes and caches length
    first_len = s.length()
    assert first_len == len(content)
    assert "_length" in s.__dict__
    assert s._length == first_len

    # Subsequent call returns cached value without recomputing
    second_len = s.length()
    assert second_len == first_len
    assert s._length == first_len
