import pytest
from string_utils.validation import is_camel_case

def test_is_camel_case_valid():
    """A properly formatted camel case string should return True."""
    assert is_camel_case("MyString") is True
    assert is_camel_case("myString123") is True
    assert is_camel_case("A1b2C3") is True

def test_is_camel_case_invalid_boundary():
    """Strings that violate camel case rules should return False."""
    # starts with a number
    assert is_camel_case("1Camel") is False
    # contains non-alphanumeric characters
    assert is_camel_case("My-String") is False
    # only lowercase letters
    assert is_camel_case("mystring") is False
    # only uppercase letters
    assert is_camel_case("MYSTRING") is False
    # empty string
    assert is_camel_case("") is False

def test_is_camel_case_non_string_input():
    """Non-string inputs should be treated as invalid and return False."""
    assert is_camel_case(None) is False
    assert is_camel_case(123) is False
    assert is_camel_case(['MyString']) is False
