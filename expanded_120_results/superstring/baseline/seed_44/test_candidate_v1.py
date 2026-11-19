import pytest
from superstring.superstring import SuperString

def test_superstring_behavior():
    s = SuperString("hello")

    # length caching
    first_len = s.length()
    assert first_len == 5
    assert hasattr(s, "_length")
    second_len = s.length()
    assert second_len == 5

    # character_at
    assert s.character_at(0) == "h"
    assert s.character_at(4) == "o"
    with pytest.raises(IndexError):
        s.character_at(5)

    # to_printable defaults
    assert s.to_printable() == "hello"

    # to_printable with indices
    assert s.to_printable(1, 4) == "ell"
    assert s.to_printable(2) == "llo"
    assert s.to_printable(end_index=3) == "hel"
