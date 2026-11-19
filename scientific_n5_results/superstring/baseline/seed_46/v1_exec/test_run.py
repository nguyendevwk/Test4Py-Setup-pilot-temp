import pytest
from superstring.superstring import SuperString

def test_superstring_behavior():
    content = "Hello, World!"
    ss = SuperString(content)

    # length caching
    assert ss.length() == len(content)
    assert hasattr(ss, "_length")
    assert ss.length() == len(content)

    # character_at
    assert ss.character_at(0) == "H"
    assert ss.character_at(-1) == "!"
    with pytest.raises(IndexError):
        ss.character_at(len(content))

    # to_printable defaults
    assert ss.to_printable() == content

    # custom slice
    assert ss.to_printable(7, 12) == "World"

    # None arguments
    assert ss.to_printable(None, None) == content
    assert ss.to_printable(None, 5) == content[:5]
    assert ss.to_printable(7, None) == content[7:]

    # out-of-range slice
    assert ss.to_printable(20, 30) == ""
