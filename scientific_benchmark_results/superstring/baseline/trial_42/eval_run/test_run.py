import pytest
from superstring.superstring import SuperString

def test_superstring_to_printable_returns_expected_substring():
    s = SuperString("Hello, World!")
    # Default indices should return the full content
    assert s.to_printable() == "Hello, World!"
    # Explicit start and end indices
    assert s.to_printable(7, 12) == "World"
    # Only start index provided
    assert s.to_printable(7) == "World!"
    # Only end index provided
    assert s.to_printable(end_index=5) == "Hello"
