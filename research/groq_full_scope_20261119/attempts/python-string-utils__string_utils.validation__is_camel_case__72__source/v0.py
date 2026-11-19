import pytest
from string_utils.validation import is_camel_case

def test_is_camel_case_valid():
    """A properly formatted camel case string should return True."""
    assert is_camel_case("MyString") is True
    assert is_camel_case("myString123") is True
    assert is_camel_case("A1B2C3") is True

def test_is_camel_case_invalid():
    """Strings that do not meet camel case rules should return False."""
    # starts with a number
    assert is_camel_case("1MyString") is False
    # all lowercase
    assert is_camel_case("mystring") is False
    # contains underscore
    assert is_camel_case("My_String") is False
    # contains non-alphanumeric character
    assert is_camel_case("MyString!") is False

def test_is_camel_case_non_string():
    """Passing a non-string input should raise a TypeError."""
    with pytest.raises(TypeError):
        is_camel_case(12345)
