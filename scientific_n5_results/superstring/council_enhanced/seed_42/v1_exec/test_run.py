import pytest
from superstring.superstring import SuperString

def test_superstring_length_and_slice():
    s = SuperString('Hello World')
    # length caching: first call sets _length, subsequent calls return same value
    first_len = s.length()
    assert first_len == 11
    assert hasattr(s, "_length")
    second_len = s.length()
    assert second_len == first_len

    # to_printable returns correct substrings
    assert s.to_printable(0, 5) == 'Hello'
    assert s.to_printable(6) == 'World'

    # __getitem__ slice returns a SuperString with expected content
    slice_s = s[0:5]
    assert isinstance(slice_s, SuperString)
    assert str(slice_s) == 'Hello'

    # __getitem__ with negative index returns correct character
    assert s[-1] == 'd'
