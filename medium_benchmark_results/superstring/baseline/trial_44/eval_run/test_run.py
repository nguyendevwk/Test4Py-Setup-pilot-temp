import pytest
from superstring.superstring import SuperString

def test_superstring_length_caching():
    content = "hello world"
    ss = SuperString(content)

    # _length should not exist before first call
    assert not hasattr(ss, "_length")

    first_len = ss.length()
    assert first_len == len(content)
    # After first call, _length is set
    assert hasattr(ss, "_length")
    assert ss._length == first_len

    # Subsequent calls return the cached value
    second_len = ss.length()
    assert second_len == first_len
    assert ss._length == first_len
