import pytest
from semantic_release.helpers import format_arg

def test_format_arg_with_regular_string():
    """format_arg should wrap a normal string in quotes and strip whitespace."""
    result = format_arg("hello world")
    assert result == "'hello world'", "Expected quoted string without surrounding spaces"

def test_format_arg_with_edge_cases():
    """format_arg should handle empty strings and strings with leading/trailing spaces."""
    empty = format_arg("")
    assert empty == "''", "Empty string should be represented as two single quotes"

    spaced = format_arg("   spaced   ")
    assert spaced == "'spaced'", "Leading/trailing spaces should be stripped before quoting"

def test_format_arg_with_non_string_types():
    """format_arg should convert non-string values to their string representation."""
    number = format_arg(42)
    assert number == "42", "Integers should be converted to string without quotes"

    boolean = format_arg(True)
    assert boolean == "True", "Booleans should be converted to string without quotes"

    none_val = format_arg(None)
    assert none_val == "None", "None should be converted to string without quotes"
