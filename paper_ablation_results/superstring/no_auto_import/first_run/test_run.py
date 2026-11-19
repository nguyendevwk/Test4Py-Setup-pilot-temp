import pytest
from superstring.superstring import SuperString

def test_superstring_to_printable_returns_expected_substrings():
    content = "Hello World"
    s = SuperString(content)

    # Default call returns the full content
    assert s.to_printable() == content
    assert isinstance(s.to_printable(), str)

    # Explicit start and end indices
    assert s.to_printable(0, 5) == "Hello"
    assert s.to_printable(6, 11) == "World"

    # Omitted start_index defaults to 0
    assert s.to_printable(end_index=5) == "Hello"

    # Omitted end_index defaults to length
    assert s.to_printable(start_index=6) == "World"

    # Both indices omitted via None explicitly
    assert s.to_printable(start_index=None, end_index=None) == content
