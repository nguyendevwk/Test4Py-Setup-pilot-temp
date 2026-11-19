import pytest
from superstring.superstring import SuperString

def test_superstring_behavior():
    s = SuperString("hello")

    # length caching
    assert s.length() == 5
    assert hasattr(s, "_length")
    assert s.length() == 5  # cached value

    # character_at
    assert s.character_at(1) == "e"
    with pytest.raises(IndexError):
        s.character_at(5)

    # to_printable defaults
    assert s.to_printable() == "hello"

    # to_printable with explicit indices
    assert s.to_printable(1, 4) == "ell"

    # to_printable with None start
    assert s.to_printable(None, 3) == "hel"

    # to_printable with None end
    assert s.to_printable(2, None) == "llo"
