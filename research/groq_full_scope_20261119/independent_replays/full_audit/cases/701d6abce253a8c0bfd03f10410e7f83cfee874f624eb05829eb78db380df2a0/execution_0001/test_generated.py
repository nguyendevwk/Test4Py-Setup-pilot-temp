import pytest
from string_utils.manipulation import camel_case_to_snake
from string_utils.errors import InvalidInputError

def test_normal_conversion():
    # Normal camel case string should be converted to snake case
    input_str = "ThisIsACamelStringTest"
    expected = "this_is_a_camel_string_test"
    assert camel_case_to_snake(input_str) == expected

def test_custom_separator_and_edge_case():
    # Custom separator and string that is already snake case should be returned unchanged
    input_str = "Already_Snake_Case"
    separator = "-"
    # Since the input is not camel case, the function should return it unchanged
    assert camel_case_to_snake(input_str, separator=separator) == input_str

def test_invalid_input_type_raises_error():
    # Passing a non-string type should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        camel_case_to_snake(12345)
