import pytest
from string_utils.manipulation import camel_case_to_snake
from string_utils.errors import InvalidInputError

def test_normal_conversion():
    # Normal camel case string should be converted to snake case
    input_str = "ThisIsACamelStringTest"
    expected = "this_is_a_camel_string_test"
    assert camel_case_to_snake(input_str) == expected

def test_custom_separator_and_edge_cases():
    # Custom separator should be used and string with consecutive capitals handled
    input_str = "HTTPRequestHandler"
    expected = "http_request_handler"
    assert camel_case_to_snake(input_str, separator='-') == "http-request-handler"
    # String that is not camel case should be returned unchanged
    not_camel = "notCamelCase"
    assert camel_case_to_snake(not_camel) == not_camel

def test_invalid_input_raises_error():
    # Non-string input should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        camel_case_to_snake(12345)
