import pytest
from semantic_release.helpers import format_arg

def test_format_arg_with_regular_string():
    """format_arg should wrap a normal string in single quotes and strip whitespace."""
    result = format_arg("  hello world  ")
    assert result == "'hello world'", f"Expected quoted string, got {result}"

def test_format_arg_with_empty_and_special_characters():
    """format_arg should handle empty strings and strings with special characters correctly."""
    # Empty string should become "''"
    assert format_arg("") == "''"
    # String with quotes and newlines should be preserved inside the outer quotes
    special = "Line1\nLine2\t'quotes'"
    expected = f"'{special.strip()}'"
    assert format_arg(special) == expected

def test_format_arg_with_non_string_types():
    """format_arg should convert non-string types to their string representation."""
    assert format_arg(123) == "123"
    assert format_arg(3.14) == "3.14"
    assert format_arg(True) == "True"
    assert format_arg(None) == "None"
