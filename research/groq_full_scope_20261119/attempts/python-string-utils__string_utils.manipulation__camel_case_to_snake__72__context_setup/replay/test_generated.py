import pytest
from string_utils.manipulation import camel_case_to_snake
from string_utils.errors import InvalidInputError

def test_normal_conversion():
    # Normal camel case to snake case with default separator
    result = camel_case_to_snake('ThisIsACamelStringTest')
    assert result == 'this_is_a_camel_string_test'
    # Ensure original string is unchanged
    assert result is not 'ThisIsACamelStringTest'

def test_custom_separator_and_edge_cases():
    # Custom separator and string that is already snake case
    original = 'already_snake_case'
    result = camel_case_to_snake(original, separator='-')
    # Should return unchanged because not camel case
    assert result == original
    # Camel case with numbers and acronyms
    mixed = 'XMLHttpRequest'
    expected = 'xml_http_request'
    assert camel_case_to_snake(mixed) == expected
    # Using custom separator on mixed string
    assert camel_case_to_snake(mixed, separator='-') == 'xml-http-request'

def test_invalid_input_raises_error():
    # Non-string input should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        camel_case_to_snake(12345)
    with pytest.raises(InvalidInputError):
        camel_case_to_snake(None)
