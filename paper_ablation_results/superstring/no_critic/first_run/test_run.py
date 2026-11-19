import pytest
from superstring.superstring import SuperString

def test_superstring_to_printable_returns_correct_substring():
    content = "Hello, World!"
    s = SuperString(content)

    # Default call returns the full string
    assert s.to_printable() == content

    # Explicit start and end indices
    assert s.to_printable(7, 12) == content[7:12]

    # Only start index provided
    assert s.to_printable(7) == content[7:]

    # Only end index provided
    assert s.to_printable(end_index=5) == content[:5]
