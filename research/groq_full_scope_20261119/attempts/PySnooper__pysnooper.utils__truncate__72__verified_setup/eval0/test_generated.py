import pytest
from pysnooper.utils import truncate

def test_truncate_short_string_returns_original():
    s = "short"
    result = truncate(s, 10)
    assert result == s, "truncate should return the original string if it fits within max_length"

def test_truncate_exact_length_no_truncation():
    s = "exactlyten"
    result = truncate(s, 10)
    assert result == s, "truncate should not modify string when length equals max_length"

def test_truncate_long_string_truncates_correctly():
    s = "abcdefghijklmnopqrstuvwxyz"
    max_len = 10
    result = truncate(s, max_len)
    # Expected: first 3 chars, ellipsis, last 3 chars
    expected = f"{s[:3]}...{s[-3:]}"
    assert result == expected, f"Expected '{expected}', got '{result}'"
    assert len(result) == max_len, "Resulting string length should match max_length"
