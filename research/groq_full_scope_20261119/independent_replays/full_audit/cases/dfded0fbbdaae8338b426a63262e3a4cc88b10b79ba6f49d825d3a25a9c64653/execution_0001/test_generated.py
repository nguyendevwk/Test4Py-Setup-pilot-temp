import pytest
from string_utils.validation import is_camel_case

def test_valid_camel_case():
    """A properly formatted camel case string should return True."""
    assert is_camel_case("MyString") is True
    assert is_camel_case("aB1cD2") is True

def test_invalid_starting_with_number():
    """Strings that start with a digit should be considered invalid."""
    assert is_camel_case("1MyString") is False
    assert is_camel_case("123abc") is False

def test_invalid_no_uppercase_or_lowercase():
    """Strings lacking either uppercase or lowercase letters are invalid."""
    assert is_camel_case("mystring") is False  # no uppercase
    assert is_camel_case("MYSTRING") is False  # no lowercase
