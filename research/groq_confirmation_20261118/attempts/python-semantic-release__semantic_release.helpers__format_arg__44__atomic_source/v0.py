import pytest
from semantic_release.helpers import format_arg

def test_format_arg_with_regular_string():
    """format_arg should wrap a non‑empty string in single quotes and strip whitespace."""
    result = format_arg("  hello world  ")
    assert result == "'hello world'"

def test_format_arg_with_empty_string():
    """format_arg should return two single quotes for an empty string."""
    result = format_arg("")
    assert result == "''"

def test_format_arg_with_non_string_value():
    """format_arg should convert non‑string values to their string representation."""
    result = format_arg(42)
    assert result == "42"
