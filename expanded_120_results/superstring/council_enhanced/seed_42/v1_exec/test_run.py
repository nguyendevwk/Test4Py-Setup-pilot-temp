import pytest
from superstring.superstring import SuperString

def test_superstring_length_caching():
    """Verify that SuperString.length() caches its result after the first call."""
    s = SuperString("hello")
    # Before calling length, the internal cache should not exist
    assert not hasattr(s, "_length"), "Cache should not exist before first length() call"

    # First call computes and stores the length
    first_len = s.length()
    assert first_len == 5, "Length should be computed correctly"
    assert hasattr(s, "_length"), "Cache should be set after first length() call"
    assert s._length == 5, "Cached length should match computed value"

    # Subsequent calls should return the cached value without recomputing
    second_len = s.length()
    assert second_len == 5, "Subsequent length() calls should return the same value"
    assert s._length == 5, "Cached length should remain unchanged after subsequent calls"
