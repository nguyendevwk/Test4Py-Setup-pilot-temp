import pytest
from apimd.parser import esc_underscore

def test_no_underscore_returns_same_string():
    """When the input contains no underscore, the string should be returned unchanged."""
    original = "no_underscore_here"
    # Count underscores: 1, so should not be escaped
    result = esc_underscore(original)
    assert result == original
    assert result is not original  # a new string object is returned

def test_multiple_underscores_are_escaped():
    """When the input contains more than one underscore, all should be escaped."""
    original = "multiple_underscores_in_this_string"
    result = esc_underscore(original)
    # All underscores should be replaced with escaped version
    assert result == "multiple\\_underscores\\_in\\_this\\_string"
    # Ensure that the original string is unchanged
    assert original == "multiple_underscores_in_this_string"

def test_single_underscore_is_not_escaped_but_other_chars_remain():
    """A single underscore should not be escaped, but other characters should stay intact."""
    original = "a_b"
    result = esc_underscore(original)
    assert result == original
    # Verify that the underscore is still present and not escaped
    assert "_" in result
    assert r"\_" not in result
