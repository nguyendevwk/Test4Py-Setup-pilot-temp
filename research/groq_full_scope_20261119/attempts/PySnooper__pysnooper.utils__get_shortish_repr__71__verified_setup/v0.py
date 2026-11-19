import pytest
from pysnooper.utils import get_shortish_repr, get_repr_function, truncate, normalize_repr

# ------------------------------------------------------------------
# Test 1: Normal behavior with default settings
# ------------------------------------------------------------------
def test_get_shortish_repr_basic():
    # Simple integer: repr is "1"
    result = get_shortish_repr(1)
    assert result == "1", "repr of integer should be unchanged"

    # String with newline: should have newlines removed
    s = "line1\nline2\rline3"
    result = get_shortish_repr(s)
    assert "\n" not in result and "\r" not in result
    assert result == "line1line2line3", "newlines should be stripped"

    # Custom repr function that returns a long string
    long_str = "a" * 50
    custom_repr = (str, lambda x: long_str)
    result = get_shortish_repr("anything", custom_repr=custom_repr)
    assert result == long_str, "custom repr should override default"

# ------------------------------------------------------------------
# Test 2: Truncation and normalization
# ------------------------------------------------------------------
def test_get_shortish_repr_truncate_and_normalize():
    # Create a string that will be truncated
    original = "0123456789"
    # Truncate to 5 characters
    truncated = get_shortish_repr(original, max_length=5)
    assert truncated == "01234", "should truncate to 5 characters"

    # Normalize: replace non-printable characters
    # Use a string with a tab and a newline
    raw = "foo\tbar\nbaz"
    normalized = get_shortish_repr(raw, normalize=True)
    # normalize_repr should replace tab with space and remove newline
    expected = normalize_repr("foo\tbar\nbaz")
    assert normalized == expected, "normalize should process control characters"

    # Combined: truncate after normalization
    combined = get_shortish_repr(raw, normalize=True, max_length=6)
    # normalize first, then truncate
    expected_combined = truncate(normalize_repr(raw), 6)
    assert combined == expected_combined, "order of normalize and truncate should be correct"

# ------------------------------------------------------------------
# Test 3: Error handling when repr function raises
# ------------------------------------------------------------------
def test_get_shortish_repr_repr_failure():
    # Define a custom repr that raises an exception
    def bad_repr(obj):
        raise RuntimeError("cannot represent")

    custom_repr = (object, bad_repr)
    # Use an object instance
    obj = object()
    result = get_shortish_repr(obj, custom_repr=custom_repr)
    assert result == "REPR FAILED", "should return placeholder on repr failure"

    # Ensure that the exception is not propagated
    try:
        get_shortish_repr(obj, custom_repr=custom_repr)
    except Exception:
        pytest.fail("get_shortish_repr should not raise exceptions")

    # Verify that the default repr function is used when custom_repr does not match type
    result_default = get_shortish_repr(obj)
    assert result_default.startswith("<object"), "default repr should be used when no custom match"
