import pytest
from apimd.parser import esc_underscore

def test_no_underscore_returns_same():
    """When the string contains no underscore, it should be returned unchanged."""
    original = "no_underscore_here"
    # Count underscores: 1, so should not be escaped
    result = esc_underscore(original)
    assert result == original
    assert result is not original  # new string object

def test_multiple_underscores_are_escaped():
    """When the string contains more than one underscore, all should be escaped."""
    original = "multiple_underscores_in_this_string"
    expected = original.replace("_", r"\_")
    result = esc_underscore(original)
    assert result == expected
    assert result.count(r"\_") == original.count("_")
    assert result.count("_") == 0

def test_boundary_single_underscore():
    """Boundary case: exactly one underscore should not be escaped."""
    original = "single_underscore"
    result = esc_underscore(original)
    assert result == original
    assert result.count(r"\_") == 0
    assert result.count("_") == 1
