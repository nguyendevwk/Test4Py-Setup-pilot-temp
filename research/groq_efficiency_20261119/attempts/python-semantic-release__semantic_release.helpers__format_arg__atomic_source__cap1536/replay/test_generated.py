import pytest
from semantic_release.helpers import format_arg

def test_format_arg_with_regular_string():
    """format_arg should wrap a non‑empty string in single quotes and strip whitespace."""
    result = format_arg("  hello world  ")
    assert result == "'hello world'", f"Expected quoted string, got {result!r}"

def test_format_arg_with_empty_string():
    """format_arg should handle an empty string correctly, returning two single quotes."""
    result = format_arg("")
    assert result == "''", f"Expected two single quotes for empty string, got {result!r}"

def test_format_arg_with_non_string_value():
    """format_arg should convert non‑string values to their string representation."""
    result = format_arg(42)
    assert result == "42", f"Expected '42', got {result!r}"
    result = format_arg(3.14)
    assert result == "3.14", f"Expected '3.14', got {result!r}"
    result = format_arg(True)
    assert result == "True", f"Expected 'True', got {result!r}"
