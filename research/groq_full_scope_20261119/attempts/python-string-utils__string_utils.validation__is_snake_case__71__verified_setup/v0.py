import pytest
from string_utils.validation import is_snake_case

def test_is_snake_case_normal():
    # Normal snake case with default separator
    assert is_snake_case("foo_bar_baz") is True
    # Mixed case and digits allowed
    assert is_snake_case("Foo123_bar") is True
    # Should be false if no separator
    assert is_snake_case("foobar") is False
    # Should be false if starts with a digit
    assert is_snake_case("1foo_bar") is False

def test_is_snake_case_custom_separator():
    # Using dash as separator
    assert is_snake_case("foo-bar-baz", separator="-") is True
    # Mixed case with dash
    assert is_snake_case("Foo-123_bar", separator="-") is True
    # No separator should still be false
    assert is_snake_case("foo-bar-baz", separator="_") is False
    # Starts with digit with dash separator
    assert is_snake_case("1foo-bar", separator="-") is False

def test_is_snake_case_boundary_and_invalid_inputs():
    # Empty string is not snake case
    assert is_snake_case("") is False
    # None input should be handled gracefully
    assert is_snake_case(None) is False
    # Non-string input should return False
    assert is_snake_case(12345) is False
    # String with special characters should be false
    assert is_snake_case("foo@bar") is False
