import pytest
from semantic_release.helpers import format_arg

def test_format_arg_with_regular_string():
    """format_arg should wrap a normal string in single quotes and strip whitespace."""
    result = format_arg("hello world")
    assert result == "'hello world'"
    # Ensure that the original string is not modified
    assert "hello world" in result
    assert result.startswith("'") and result.endswith("'")

def test_format_arg_with_edge_cases():
    """format_arg should handle empty strings and strings with leading/trailing spaces."""
    # Empty string
    empty = format_arg("")
    assert empty == "''"
    # Leading/trailing spaces
    spaced = format_arg("  spaced  ")
    assert spaced == "'spaced'"
    # String containing quotes should be preserved inside the outer quotes
    quoted = format_arg("O'Reilly")
    assert quoted == "'O'Reilly'"

def test_format_arg_with_non_string_types():
    """format_arg should convert non-string types to their string representation."""
    # Integer
    assert format_arg(42) == "42"
    # Float
    assert format_arg(3.14) == "3.14"
    # Boolean
    assert format_arg(True) == "True"
    # None
    assert format_arg(None) == "None"
    # List
    assert format_arg([1, 2]) == "[1, 2]"
