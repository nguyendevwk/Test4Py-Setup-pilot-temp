import pytest
from superstring.superstring import SuperString

def test_superstring_length_and_printable_and_slice():
    content = "Hello, World!"
    s = SuperString(content)

    # length caching and correctness
    assert s.length() == len(content)
    assert hasattr(s, "_length")

    # to_printable defaults to full content
    assert s.to_printable() == content

    # to_printable with explicit start and end indices
    assert s.to_printable(7, 12) == content[7:12]

    # __getitem__ with a slice returns a substring whose string representation matches
    sub = s[7:12]
    assert str(sub) == content[7:12]

    # __getitem__ with negative indices works correctly
    sub_neg = s[-6:-1]
    assert str(sub_neg) == content[-6:-1]
