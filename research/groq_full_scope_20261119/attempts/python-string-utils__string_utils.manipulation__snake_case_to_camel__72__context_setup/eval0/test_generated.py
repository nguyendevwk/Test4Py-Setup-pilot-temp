import pytest
from string_utils.manipulation import snake_case_to_camel
from string_utils.errors import InvalidInputError

def test_normal_conversion_uppercase_first():
    # Normal snake case to camel case with default upper_case_first=True
    result = snake_case_to_camel("the_snake_is_green")
    assert result == "TheSnakeIsGreen"
    # Verify that each token is capitalized correctly
    assert result[0].isupper()
    assert result[4].isupper()  # 'Snake'
    assert result[9].isupper()  # 'Is'
    assert result[12].isupper()  # 'Green'

def test_conversion_lowercase_first_and_custom_separator():
    # Convert with lower_case_first and a custom separator
    result = snake_case_to_camel("my_custom_separator", upper_case_first=False, separator="_")
    assert result == "myCustomSeparator"
    # Ensure first letter is lowercase
    assert result[0].islower()
    # Ensure subsequent tokens start with uppercase
    assert result[2].isupper()  # 'Custom'
    assert result[8].isupper()  # 'Separator'

def test_invalid_input_and_non_snake_case():
    # Passing a non-string should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        snake_case_to_camel(12345)  # type: ignore[arg-type]

    # Passing a string that is not snake case should return the original string
    original = "NotSnakeCase"
    result = snake_case_to_camel(original)
    assert result == original
    # Ensure that the function does not alter the string
    assert result is original
