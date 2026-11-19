import pytest
from superstring.superstring import SuperString

def test_superstring_length_caching():
    content = "Hello, World!"
    ss = SuperString(content)

    # First call should compute and store length
    first_len = ss.length()
    assert isinstance(first_len, int)
    assert first_len == len(content)
    assert hasattr(ss, "_length")
    assert ss._length == first_len

    # Subsequent call should return cached value without recomputation
    second_len = ss.length()
    assert second_len == first_len
    # Ensure the cached value remains unchanged
    assert ss._length == first_len
