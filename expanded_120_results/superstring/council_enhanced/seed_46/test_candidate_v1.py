import pytest
from superstring.superstring import SuperString

def test_superstring_basic_behavior():
    content = "Hello World"
    s = SuperString(content)
    # length
    assert s.length() == len(content)
    assert hasattr(s, "_length")
    # character_at
    assert s.character_at(0) == 'H'
    assert s.character_at(6) == 'W'
    # to_printable default
    assert s.to_printable() == content
    # to_printable slice
    assert s.to_printable(6, 11) == "World"
    # __getitem__ slice
    slice_obj = s[6:11]
    assert isinstance(slice_obj, SuperString)
    assert str(slice_obj) == "World"
    # __getitem__ negative index
    assert s[-1] == 'd'
