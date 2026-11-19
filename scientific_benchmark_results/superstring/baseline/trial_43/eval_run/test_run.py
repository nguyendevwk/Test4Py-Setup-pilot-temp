import pytest
from superstring.superstring import SuperString

def test_superstring_to_printable_returns_expected_substring():
    content = "Hello, World!"
    ss = SuperString(content)

    # Default parameters should return the full content
    assert ss.to_printable() == content

    # Explicit start and end indices should return the correct slice
    assert ss.to_printable(7, 12) == "World"

    # Passing None for start_index should default to 0
    assert ss.to_printable(None, 5) == content[:5]

    # Passing None for end_index should default to the string length
    assert ss.to_printable(7, None) == content[7:]
