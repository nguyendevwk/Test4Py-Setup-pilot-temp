import pytest
from pysnooper.utils import truncate

def test_truncate_short_string_returns_original():
    """When the string length is less than or equal to max_length, the original string is returned."""
    original = "short"
    result = truncate(original, 10)
    assert result is original  # same object for short strings
    assert result == "short"

def test_truncate_exact_boundary_no_truncation():
    """When the string length equals max_length, no truncation occurs."""
    original = "exactlyten"
    result = truncate(original, 10)
    assert result == original
    assert result == "exactlyten"

def test_truncate_long_string_splits_correctly():
    """When the string is longer than max_length, it is truncated with ellipsis in the middle."""
    original = "abcdefghijklmnopqrstuvwxyz"
    max_len = 15
    result = truncate(original, max_len)
    # Expected: left part 6 chars, ellipsis, right part 6 chars
    expected = "abcdef...uvwxyz"
    assert result == expected
    assert len(result) == max_len
    assert result.startswith("abcdef")
    assert result.endswith("uvwxyz")
    assert "..." in result
