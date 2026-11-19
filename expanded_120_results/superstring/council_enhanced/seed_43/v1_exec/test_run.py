import pytest
from superstring.superstring import SuperString

def test_superstring_length_caching():
    content = "Hello, World!"
    s = SuperString(content)

    # First call should compute and cache the length
    first_length = s.length()
    assert isinstance(first_length, int), "length() should return an int"
    assert first_length == len(content), "length() should equal len(content)"
    assert hasattr(s, "_length"), "SuperString should cache length in _length attribute"
    assert s._length == len(content), "_length should match the computed length"

    # Subsequent calls should return the cached value without recomputing
    second_length = s.length()
    assert second_length == first_length, "Subsequent length() calls should return the same value"
    assert s._length == first_length, "_length should remain unchanged after subsequent calls"
