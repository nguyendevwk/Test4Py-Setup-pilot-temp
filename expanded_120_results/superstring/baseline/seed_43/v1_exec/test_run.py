import pytest
from superstring.superstring import SuperString

def test_superstring_to_printable_substring():
    content = "abcdefghijklmnopqrstuvwxyz"
    ss = SuperString(content)

    # Default slice uses full content
    assert ss.to_printable() == content

    # Slice from a start index to the end
    assert ss.to_printable(5) == content[5:]

    # Slice from the start to an end index
    assert ss.to_printable(end_index=10) == content[:10]

    # Slice between two indices
    assert ss.to_printable(3, 8) == content[3:8]

    # Verify that length is used for default end
    assert ss.to_printable() == content[:ss.length()]
