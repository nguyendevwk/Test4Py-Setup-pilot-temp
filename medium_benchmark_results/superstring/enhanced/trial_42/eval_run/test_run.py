import pytest
from superstring.superstring import SuperString

def test_superstring_to_printable_returns_expected_substring():
    content = "Hello World"
    s = SuperString(content)

    # Default indices should return the full string
    assert s.to_printable() == content

    # Explicit start and end indices should return the correct slice
    assert s.to_printable(6, 11) == "World"
    assert s.to_printable(0, 5) == "Hello"

    # Omit end_index to use the full length
    assert s.to_printable(6) == "World"

    # Verify that the length method reports the correct size
    assert s.length() == len(content)
