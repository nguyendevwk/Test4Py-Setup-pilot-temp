import pytest
from string_utils.manipulation import snake_case_to_camel
from string_utils.errors import InvalidInputError

def test_normal_conversion_uppercase_first():
    # Normal snake case to camel case with default upper_case_first=True
    result = snake_case_to_camel("the_snake_is_green")
    assert result == "TheSnakeIsGreen"
    # Verify that each token is capitalized
    assert result[0].isupper()
    assert result[4].isupper()  # 'Snake'
    assert result[9].isupper()  # 'Is'
    assert result[12].isupper()  # 'Green'

def test_conversion_lowercase_first_and_custom_separator():
    # Convert with lower_case_first and a custom separator
    result = snake_case_to_camel("my-custom-string", upper_case_first=False, separator="-")
    assert result == "myCustomString"
    # First character should be lowercase
    assert result[0].islower()
    # Subsequent tokens should start with uppercase
    assert result[2].isupper()  # 'Custom'
    assert result[8].isupper()  # 'String'

def test_invalid_input_and_non_snake_case():
    # Passing a non-string should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        snake_case_to_camel(12345)  # type: ignore[arg-type]

    # Passing a string that is not snake case should return the original string
    original = "ThisIsNotSnakeCase"
    result = snake_case_to_camel(original)
    assert result == original
    # Ensure that the function did not alter the string
    assert result is original
