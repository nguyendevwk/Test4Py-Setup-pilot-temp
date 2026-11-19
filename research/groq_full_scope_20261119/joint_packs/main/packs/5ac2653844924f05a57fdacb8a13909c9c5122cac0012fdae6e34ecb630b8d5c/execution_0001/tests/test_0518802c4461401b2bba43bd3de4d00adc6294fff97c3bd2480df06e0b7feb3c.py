import pytest
from string_utils.validation import is_snake_case

def test_is_snake_case_valid_and_invalid_strings():
    # Valid snake case with default separator
    assert is_snake_case("foo_bar_baz") is True
    # Invalid: no separator
    assert is_snake_case("foobar") is False
    # Invalid: starts with a digit
    assert is_snake_case("1foo_bar") is False
    # Invalid: contains uppercase letters but still allowed by regex
    assert is_snake_case("Foo_Bar") is True  # regex is case-insensitive

def test_is_snake_case_with_dash_separator():
    # Valid snake case using dash separator
    assert is_snake_case("foo-bar-baz", separator="-") is True
    # Invalid: missing separator
    assert is_snake_case("foobar", separator="-") is False
    # Invalid: starts with a digit even with dash separator
    assert is_snake_case("1foo-bar", separator="-") is False

def test_is_snake_case_non_string_input():
    # Non-string input should return False without raising
    assert is_snake_case(12345) is False
    assert is_snake_case(None) is False
    assert is_snake_case(["foo", "bar"]) is False
