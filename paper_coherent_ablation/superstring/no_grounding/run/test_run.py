import pytest
from superstring.superstring import SuperString

def test_superstring_to_printable_slicing_behavior():
    s = SuperString("hello world")
    # Default parameters should return the full content
    assert s.to_printable() == "hello world"
    # Explicit start index with default end should return suffix
    assert s.to_printable(6) == "world"
    # Explicit start and end indices should return the specified slice
    assert s.to_printable(0, 5) == "hello"
    assert s.to_printable(6, 11) == "world"
    # Empty slice when start == end
    assert s.to_printable(6, 6) == ""
    # Passing None explicitly should behave like default parameters
    assert s.to_printable(None, None) == "hello world"
