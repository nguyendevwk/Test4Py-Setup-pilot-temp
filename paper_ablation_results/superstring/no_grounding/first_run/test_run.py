import pytest
from superstring.superstring import SuperString

def test_superstring_length_caches_value():
    content = "hello"
    s = SuperString(content)

    # First call should compute and store the length
    first_len = s.length()
    assert first_len == len(content)
    assert hasattr(s, "_length")
    assert s._length == len(content)

    # Subsequent call should return the cached value without recomputing
    second_len = s.length()
    assert second_len == first_len
    assert s._length == first_len
