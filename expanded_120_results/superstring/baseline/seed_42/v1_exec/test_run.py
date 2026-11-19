import pytest
from superstring.superstring import SuperString

def test_superstring_to_printable_behavior():
    content = "Hello, World!"
    ss = SuperString(content)

    # Default slicing returns the whole content
    assert ss.to_printable() == content

    # Specifying only start_index
    assert ss.to_printable(start_index=7) == content[7:]

    # Specifying only end_index
    assert ss.to_printable(end_index=5) == content[:5]

    # Specifying both start_index and end_index
    assert ss.to_printable(start_index=7, end_index=12) == content[7:12]

    # start_index greater than end_index yields an empty string
    assert ss.to_printable(start_index=12, end_index=7) == ""

    # Negative indices work as expected
    assert ss.to_printable(start_index=-5, end_index=-1) == content[-5:-1]
