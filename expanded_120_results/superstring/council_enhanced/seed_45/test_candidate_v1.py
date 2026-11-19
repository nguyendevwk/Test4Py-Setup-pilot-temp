import pytest
from superstring.superstring import SuperString

def test_superstring_basic_behavior():
    s = SuperString('Hello, World!')

    # length caching
    assert s.length() == 13
    assert hasattr(s, "_length")

    # character_at
    assert s.character_at(0) == 'H'
    assert s.character_at(7) == 'W'

    # to_printable default and with indices
    assert s.to_printable() == 'Hello, World!'
    assert s.to_printable(7, 12) == 'World'

    # __getitem__ slice returns a SuperString with correct content
    sub = s[7:12]
    assert isinstance(sub, SuperString)
    assert str(sub) == 'World'
    assert sub.length() == 5

    # __getitem__ negative index returns correct character
    assert s[-1] == '!'
