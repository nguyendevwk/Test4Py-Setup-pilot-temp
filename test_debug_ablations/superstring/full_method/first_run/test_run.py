import pytest
from superstring.superstring import SuperString

def test_superstring_length_caching():
    s = SuperString("abc")
    # First call should compute and store _length
    first_len = s.length()
    assert first_len == 3
    assert hasattr(s, "_length")
    assert s._length == 3
    # Subsequent call should return the cached value without recomputing
    second_len = s.length()
    assert second_len == 3
    assert s._length == 3
