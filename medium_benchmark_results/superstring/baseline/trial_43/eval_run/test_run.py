import pytest
from superstring.superstring import SuperString

def test_superstring_length_and_substring():
    s = SuperString("hello world")
    # length caches the computed value
    assert not hasattr(s, "_length")
    first_len = s.length()
    assert first_len == 11
    assert hasattr(s, "_length")
    second_len = s.length()
    assert second_len == first_len

    # character_at returns the correct character
    assert s.character_at(0) == "h"
    assert s.character_at(6) == "w"

    # to_printable returns the full string by default
    assert s.to_printable() == "hello world"

    # to_printable with explicit indices
    assert s.to_printable(6, 11) == "world"

    # out-of-range index raises IndexError
    with pytest.raises(IndexError):
        s.character_at(100)
