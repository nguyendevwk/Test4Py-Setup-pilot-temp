import pytest
from superstring.superstring import SuperString, SuperStringSubstring, SUPERSTRING_MINIMAL_LENGTH

def test_substring_behavior():
    # Short string: substring of full range returns the same instance
    short = SuperString("abc")
    assert short.substring(0) is short
    assert short.substring(0, short.length()) is short

    # Long string: partial range of length >= SUPERSTRING_MINIMAL_LENGTH returns a Substring instance
    long_content = "a" * 50
    long = SuperString(long_content)
    sub = long.substring(0, SUPERSTRING_MINIMAL_LENGTH)  # length 48
    assert isinstance(sub, SuperStringSubstring)
    assert sub.length() == SUPERSTRING_MINIMAL_LENGTH
    assert sub.to_printable() == long_content[:SUPERSTRING_MINIMAL_LENGTH]

    # Full range on long string returns the original instance
    assert long.substring(0, long.length()) is long
    assert long.substring(0) is long
