import pytest
from string_utils.manipulation import camel_case_to_snake
from string_utils.errors import InvalidInputError

def test_normal_conversion():
    # Normal camel case to snake case with default separator
    result = camel_case_to_snake('ThisIsACamelStringTest')
    assert result == 'this_is_a_camel_string_test'
    # Ensure original string is unchanged
    assert result is not 'ThisIsACamelStringTest'

def test_custom_separator_and_boundary():
    # Use a custom separator and test boundary conditions
    result = camel_case_to_snake('XMLHttpRequest', separator='-')
    assert result == 'xml-http-request'
    # Empty string should return empty string
    assert camel_case_to_snake('') == ''
    # String that is not camel case should be returned unchanged
    assert camel_case_to_snake('snake_case') == 'snake_case'

def test_invalid_input_raises_error():
    # Passing a non-string should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        camel_case_to_snake(12345)
    # Passing a list should also raise the same error
    with pytest.raises(InvalidInputError):
        camel_case_to_snake(['not', 'a', 'string'])
