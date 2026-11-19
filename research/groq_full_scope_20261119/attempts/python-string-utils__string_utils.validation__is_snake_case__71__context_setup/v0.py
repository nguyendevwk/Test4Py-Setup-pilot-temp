import pytest
from string_utils.validation import is_snake_case

def test_is_snake_case_normal():
    # Valid snake case strings
    assert is_snake_case("foo_bar") is True
    assert is_snake_case("Foo_Bar_123") is True
    assert is_snake_case("foo-bar", separator="-") is True
    # Invalid because no separator
    assert is_snake_case("foobar") is False
    # Invalid because starts with a digit
    assert is_snake_case("1foo_bar") is False
    # Invalid because contains invalid characters
    assert is_snake_case("foo@bar") is False

def test_is_snake_case_boundary():
    # Empty string or non-string input should return False
    assert is_snake_case("") is False
    assert is_snake_case(" ") is False
    assert is_snake_case(None) is False
    # String with only separator
    assert is_snake_case("_") is False
    # String with separator but no letters
    assert is_snake_case("__") is False
    # String with separator and letters but leading separator
    assert is_snake_case("_foo_bar") is False

def test_is_snake_case_error_behavior():
    # Passing a non-string type should not raise an exception
    assert is_snake_case(123) is False
    assert is_snake_case([1, 2, 3]) is False
    # Passing a separator that is not a single character should still work
    assert is_snake_case("foo__bar", separator="__") is True
    # Passing a separator that is not in the predefined map
    assert is_snake_case("foo|bar", separator="|") is True
