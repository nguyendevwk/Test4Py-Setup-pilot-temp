import pytest
from string_utils.validation import is_camel_case

def test_is_camel_case_valid():
    """A correctly formatted camel case string should return True."""
    assert is_camel_case("MyString") is True
    assert is_camel_case("myString123") is True
    assert is_camel_case("A1B2C3") is True

def test_is_camel_case_invalid_boundary():
    """Strings that violate boundary conditions should return False."""
    # starts with a number
    assert is_camel_case("1MyString") is False
    # contains only lowercase letters
    assert is_camel_case("mystring") is False
    # contains only uppercase letters
    assert is_camel_case("MYSTRING") is False
    # contains non-alphanumeric characters
    assert is_camel_case("My_String") is False

def test_is_camel_case_non_string_input():
    """Non-string inputs should be handled gracefully and return False."""
    assert is_camel_case(12345) is False
    assert is_camel_case(None) is False
    assert is_camel_case(["MyString"]) is False
