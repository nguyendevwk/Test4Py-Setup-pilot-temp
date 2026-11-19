import pytest
from string_utils.validation import is_snake_case

def test_is_snake_case_valid_and_invalid_examples():
    # Valid snake case with default separator
    assert is_snake_case("foo_bar_baz") is True
    # Invalid: no separator
    assert is_snake_case("foobar") is False
    # Invalid: starts with a digit
    assert is_snake_case("1foo_bar") is False
    # Invalid: contains uppercase letters but still snake case allowed
    assert is_snake_case("Foo_Bar") is True
    # Invalid: contains special character
    assert is_snake_case("foo-bar") is False

def test_is_snake_case_custom_separator_and_edge_cases(tmp_path):
    # Custom separator '-'
    assert is_snake_case("foo-bar-baz", separator="-") is True
    # Custom separator with no separator present
    assert is_snake_case("foobar", separator="-") is False
    # Edge case: separator at start
    assert is_snake_case("-foo_bar", separator="-") is True
    # Edge case: separator at end
    assert is_snake_case("foo_bar-", separator="-") is True
    # Edge case: multiple separators in a row
    assert is_snake_case("foo__bar", separator="_") is True

def test_is_snake_case_non_string_inputs():
    # Non-string inputs should return False
    assert is_snake_case(12345) is False
    assert is_snake_case(None) is False
    assert is_snake_case(["foo", "bar"]) is False
    # Empty string is not a full string
    assert is_snake_case("") is False
