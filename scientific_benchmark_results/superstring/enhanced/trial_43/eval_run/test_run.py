import pytest
from superstring.superstring import SuperString

def test_superstring_to_printable_substring():
    content = "Hello, World!"
    s = SuperString(content)

    # Default slice returns the full content
    assert s.to_printable() == content
    assert isinstance(s.to_printable(), str)

    # Explicit start and end indices
    assert s.to_printable(7, 12) == "World"

    # Only start index provided
    assert s.to_printable(7) == content[7:]

    # Only end index provided
    assert s.to_printable(end_index=5) == content[:5]

    # Negative indices behave like Python slicing
    assert s.to_printable(-6, -1) == content[-6:-1]
