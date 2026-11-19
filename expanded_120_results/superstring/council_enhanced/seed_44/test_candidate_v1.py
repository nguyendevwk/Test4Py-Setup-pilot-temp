import pytest
from superstring.superstring import SuperString

def test_superstring_basic_behavior():
    s = SuperString("Hello World")

    # length caching
    assert s.length() == 11
    assert hasattr(s, "_length")
    assert s._length == 11

    # to_printable defaults and slicing
    assert s.to_printable() == "Hello World"
    assert s.to_printable(6, 11) == "World"

    # character_at
    assert s.character_at(0) == "H"
    assert s.character_at(6) == "W"

    # __len__ and __str__
    assert len(s) == 11
    assert str(s) == "Hello World"

    # __getitem__ slice returns a SuperString with correct content
    sub = s[6:11]
    assert isinstance(sub, SuperString)
    assert str(sub) == "World"

    # negative indices slice
    sub_neg = s[-5:]
    assert isinstance(sub_neg, SuperString)
    assert str(sub_neg) == "World"
