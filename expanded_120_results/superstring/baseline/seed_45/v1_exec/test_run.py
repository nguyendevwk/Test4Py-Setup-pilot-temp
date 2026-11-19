import pytest
from superstring.superstring import SuperString

def test_superstring_behavior():
    s = SuperString("hello world")
    # length caching
    first_len = s.length()
    assert first_len == 11
    s._content = "changed"
    assert s.length() == 11  # cached value unchanged

    # character_at
    assert s.character_at(0) == 'h'
    assert s.character_at(6) == 'w'

    # to_printable defaults
    assert s.to_printable() == "hello world"

    # to_printable with explicit slice
    assert s.to_printable(6, 11) == "world"
    assert s.to_printable(6) == "world"
    assert s.to_printable(end_index=5) == "hello"
