import pytest
from semantic_release.helpers import format_arg

def test_format_arg_with_plain_string():
    """String values should be quoted and stripped of surrounding whitespace."""
    assert format_arg("hello") == "'hello'"
    assert format_arg("  world  ") == "'world'"

def test_format_arg_with_empty_and_whitespace_string():
    """Empty strings and strings containing only whitespace should be quoted as ''."""
    assert format_arg("") == "''"
    assert format_arg("   ") == "''"

def test_format_arg_with_non_string_values():
    """Non-string values should be converted to their string representation without quotes."""
    assert format_arg(42) == "42"
    assert format_arg(3.14) == "3.14"
    assert format_arg(None) == "None"
