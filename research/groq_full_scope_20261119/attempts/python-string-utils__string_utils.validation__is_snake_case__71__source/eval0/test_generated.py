import pytest
from string_utils.validation import is_snake_case

def test_valid_snake_case_returns_true():
    # Normal snake case with default separator
    assert is_snake_case("foo_bar_baz") is True
    # Snake case with custom separator
    assert is_snake_case("foo-bar-baz", separator="-") is True
    # Snake case containing digits but not starting with a digit
    assert is_snake_case("foo2_bar3") is True

def test_boundary_cases_return_false():
    # No separator present
    assert is_snake_case("foobar") is False
    # Starts with a digit
    assert is_snake_case("1foo_bar") is False
    # Separator at the start
    assert is_snake_case("_foo_bar") is False
    # Separator at the end
    assert is_snake_case("foo_bar_") is False

def test_invalid_input_type_returns_false():
    # Non-string input should return False, not raise an exception
    assert is_snake_case(12345) is False
    assert is_snake_case(None) is False
    assert is_snake_case(["foo", "bar"]) is False
