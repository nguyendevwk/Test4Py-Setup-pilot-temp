import pytest
from superstring.superstring import SuperString

def test_superstring_to_printable_and_length_cache():
    content = "Hello World"
    s = SuperString(content)

    # length() should compute and cache the value
    assert s.length() == len(content)
    assert hasattr(s, "_length") and s._length == len(content)

    # to_printable() without arguments returns the full string
    full = s.to_printable()
    assert isinstance(full, str) and full == content

    # to_printable(start_index) returns substring from start_index to end
    suffix = s.to_printable(6)
    assert suffix == content[6:]

    # to_printable(start_index, end_index) returns slice
    prefix = s.to_printable(0, 5)
    assert prefix == content[:5]

    # start_index > end_index yields empty string
    empty = s.to_printable(5, 3)
    assert empty == ""
