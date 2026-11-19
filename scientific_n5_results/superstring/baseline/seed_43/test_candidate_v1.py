import pytest
from superstring.superstring import SuperString

def test_superstring_length_and_to_printable():
    s = SuperString("hello")
    # length should compute and cache the value
    first_len = s.length()
    assert first_len == 5
    assert hasattr(s, "_length") and s._length == 5
    # subsequent calls return the cached value
    assert s.length() == 5

    # to_printable defaults to full content
    assert s.to_printable() == "hello"

    # slice with explicit indices
    assert s.to_printable(1, 4) == "ell"
    # slice with only end_index
    assert s.to_printable(end_index=3) == "hel"
    # slice with only start_index
    assert s.to_printable(start_index=2) == "llo"

    # character_at returns correct character
    assert s.character_at(0) == "h"
    assert s.character_at(4) == "o"

    # out-of-range index raises IndexError
    with pytest.raises(IndexError):
        s.character_at(5)
