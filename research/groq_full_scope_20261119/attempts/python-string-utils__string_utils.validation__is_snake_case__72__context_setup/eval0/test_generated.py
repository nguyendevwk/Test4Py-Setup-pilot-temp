import pytest
from string_utils.validation import is_snake_case

def test_is_snake_case_normal():
    # Valid snake case with default separator
    assert is_snake_case("foo_bar_baz") is True
    # Valid snake case with numbers and mixed case
    assert is_snake_case("Foo123_bar") is True
    # Invalid: no separator
    assert is_snake_case("foobar") is False
    # Invalid: starts with a digit
    assert is_snake_case("1foo_bar") is False
    # Invalid: contains invalid characters
    assert is_snake_case("foo-bar_baz") is False

def test_is_snake_case_custom_separator():
    # Valid snake case with custom separator '-'
    assert is_snake_case("foo-bar-baz", separator="-") is True
    # Invalid: using default separator but string contains '-'
    assert is_snake_case("foo-bar_baz") is False
    # Invalid: custom separator not present
    assert is_snake_case("foo_bar_baz", separator="-") is False

def test_is_snake_case_boundary_and_error():
    # Boundary: empty string
    assert is_snake_case("") is False
    # Boundary: string with only spaces
    assert is_snake_case("   ") is False
    # Error: non-string input should return False, not raise
    assert is_snake_case(123) is False
    assert is_snake_case(None) is False
