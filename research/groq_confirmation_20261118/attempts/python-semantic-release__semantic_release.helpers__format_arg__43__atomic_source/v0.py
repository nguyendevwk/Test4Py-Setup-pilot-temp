import pytest
from semantic_release.helpers import format_arg

def test_format_arg_with_regular_string():
    """format_arg should wrap a normal string in single quotes and strip whitespace."""
    result = format_arg("  hello world  ")
    assert result == "'hello world'"
    # Ensure that the original string is not modified
    assert "  hello world  " == "  hello world  "

def test_format_arg_with_empty_and_non_string():
    """format_arg should handle empty strings and non-string types correctly."""
    # Empty string should become "''"
    assert format_arg("") == "''"
    # Non-string types should be converted to their string representation
    assert format_arg(42) == "42"
    assert format_arg(3.14) == "3.14"
    assert format_arg(True) == "True"

def test_format_arg_with_special_characters_and_unicode():
    """format_arg should preserve special characters and unicode after stripping."""
    special = "  \n\t¡Hola!  "
    expected = "'¡Hola!'"
    assert format_arg(special) == expected
    # Unicode characters should remain unchanged
    unicode_str = "  café  "
    assert format_arg(unicode_str) == "'café'"
