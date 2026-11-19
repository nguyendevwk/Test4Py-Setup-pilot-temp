import pytest
from superstring.superstring import SuperString

def test_superstring_basic_behavior():
    content = "Hello, World!"
    s = SuperString(content)

    # length caching
    assert s.length() == len(content)
    assert hasattr(s, "_length")
    first_length = s._length
    assert s.length() == first_length

    # character_at
    assert s.character_at(7) == "W"

    # to_printable default
    assert s.to_printable() == content

    # to_printable with indices
    assert s.to_printable(7, 12) == content[7:12]

    # slice via __getitem__
    sub = s[7:12]
    assert isinstance(sub, SuperString)
    assert str(sub) == content[7:12]

    # negative indices slice
    neg_sub = s[-6:-1]
    assert isinstance(neg_sub, SuperString)
    assert str(neg_sub) == content[-6:-1]
