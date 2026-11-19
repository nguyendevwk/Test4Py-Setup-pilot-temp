import pytest
from apimd.parser import esc_underscore

def test_no_underscore_returns_same():
    """When the string contains no underscore, it should be returned unchanged."""
    original = "no_underscore_here"  # one underscore
    result = esc_underscore(original)
    assert result == original, "String with a single underscore should not be escaped"

def test_multiple_underscores_are_escaped():
    """When the string contains more than one underscore, all should be escaped."""
    original = "multiple_underscores_in_this_string"
    expected = original.replace("_", r"\_")
    result = esc_underscore(original)
    assert result == expected, "All underscores should be escaped when count > 1"

def test_edge_case_single_underscore_at_end():
    """A single underscore at the end of the string should not be escaped."""
    original = "trailing_"
    result = esc_underscore(original)
    assert result == original, "Trailing single underscore should not be escaped"
