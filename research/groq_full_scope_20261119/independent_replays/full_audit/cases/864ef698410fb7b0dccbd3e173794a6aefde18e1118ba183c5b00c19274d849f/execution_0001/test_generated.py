import pytest
from semantic_release.helpers import format_arg


def test_format_arg_with_regular_string():
    """String values should be wrapped in single quotes and stripped."""
    result = format_arg("  hello world  ")
    assert result == "'hello world'"


def test_format_arg_with_empty_and_whitespace_string():
    """Empty or whitespace-only strings should be stripped and wrapped."""
    result_empty = format_arg("")
    result_space = format_arg("   ")
    assert result_empty == "''"
    assert result_space == "''"


def test_format_arg_with_non_string_values():
    """Non-string values should be converted to their string representation."""
    assert format_arg(123) == "123"
    assert format_arg(3.14) == "3.14"
    assert format_arg(True) is True or format_arg(True) == "True"
