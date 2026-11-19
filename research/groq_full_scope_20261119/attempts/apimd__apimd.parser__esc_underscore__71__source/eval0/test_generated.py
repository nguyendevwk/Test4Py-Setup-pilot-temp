import pytest
from apimd.parser import esc_underscore

def test_escape_multiple_underscores():
    """When a string contains more than one underscore, all underscores are escaped."""
    original = "foo_bar_baz_qux"
    expected = r"foo\_bar\_baz\_qux"
    result = esc_underscore(original)
    assert result == expected
    # Ensure that the number of backslashes matches the number of underscores
    assert result.count(r"\_") == original.count('_')
    # The original string should remain unchanged
    assert original == "foo_bar_baz_qux"

def test_no_escape_single_or_no_underscore():
    """When a string contains zero or one underscore, it is returned unchanged."""
    # Zero underscores
    zero = "foobar"
    assert esc_underscore(zero) == zero
    # One underscore
    one = "foo_bar"
    assert esc_underscore(one) == one
    # Ensure no escape characters are added
    assert r"\_" not in esc_underscore(zero)
    assert r"\_" not in esc_underscore(one)

def test_escape_with_special_characters():
    """Escaping should not affect other characters or escape sequences."""
    mixed = "a_b_c!@#_123"
    # Count underscores: 3 > 1, so all should be escaped
    escaped = esc_underscore(mixed)
    assert escaped == r"a\_b\_c!@#\_123"
    # Verify that other characters remain intact
    assert escaped.replace(r"\_", "") == "a_b_c!@#_123".replace("_", "")
    # Ensure that backslashes are only introduced before underscores
    assert all(ch == "\\" or ch == "_" or ch.isalnum() or ch in "!@#" for ch in escaped)
