import pytest
from string_utils.manipulation import snake_case_to_camel
from string_utils.errors import InvalidInputError

def test_normal_conversion_uppercase_first():
    # Normal snake case to camel case with default upper_case_first=True
    result = snake_case_to_camel("the_snake_is_green")
    assert result == "TheSnakeIsGreen"
    # Verify that each word is capitalized
    assert result[0].isupper()
    assert "Snake" in result
    assert "Green" in result

def test_boundary_invalid_snake_case_returns_original():
    # Input that is not valid snake case should be returned unchanged
    input_str = "TheSnakeIsGreen"  # camel case, not snake case
    result = snake_case_to_camel(input_str, separator="_")
    assert result == input_str
    # Ensure no transformation occurs
    assert result == "TheSnakeIsGreen"

def test_error_non_string_input_raises():
    # Passing a non-string should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        snake_case_to_camel(12345)  # type: ignore[arg-type]
