import pytest
from superstring.superstring import SuperString

def test_superstring_behavior():
    s = SuperString("hello")

    # length caching
    assert s.length() == 5
    assert hasattr(s, "_length")
    s._length = 999
    assert s.length() == 999  # uses cached value

    # character_at
    assert s.character_at(1) == "e"
    with pytest.raises(IndexError):
        s.character_at(10)

    # to_printable defaults and slices
    assert s.to_printable() == "hello"
    assert s.to_printable(1, 4) == "ell"
    assert s.to_printable(3) == "lo"
    assert s.to_printable(end_index=2) == "he"
    assert s.to_printable(4, 3) == ""  # start > end yields empty string
