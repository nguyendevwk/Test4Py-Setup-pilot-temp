import pytest
from superstring.superstring import SuperString

def test_superstring_length_caching():
    s = SuperString("hello")
    # First call computes and caches length
    first_len = s.length()
    assert first_len == 5
    assert hasattr(s, "_length") and s._length == 5
    # Subsequent call returns cached value
    second_len = s.length()
    assert second_len == 5
    # Changing content after caching does not affect cached length
    s._content = "world!"
    assert s.length() == 5
