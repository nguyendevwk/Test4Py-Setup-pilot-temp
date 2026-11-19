import pytest
from string_utils.manipulation import snake_case_to_camel
from string_utils.errors import InvalidInputError

def test_normal_conversion_with_default_uppercase():
    # Normal snake case string with default separator and uppercase first letter
    result = snake_case_to_camel("the_snake_is_green")
    assert result == "TheSnakeIsGreen"

def test_boundary_empty_string_returns_empty():
    # Empty string is a valid string but not a snake case; should be returned unchanged
    result = snake_case_to_camel("")
    assert result == ""

def test_error_non_string_input_raises_invalid_input_error():
    # Passing a non-string type should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        snake_case_to_camel(12345)
