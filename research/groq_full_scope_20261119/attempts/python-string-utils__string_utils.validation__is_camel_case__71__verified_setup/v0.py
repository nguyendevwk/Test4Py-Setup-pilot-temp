import pytest
from string_utils.validation import is_camel_case

def test_valid_camel_case():
    # A typical camel case string with letters and numbers
    assert is_camel_case("MyString123") is True
    # Mixed case with no leading number
    assert is_camel_case("aB") is True
    # Edge case: single uppercase letter (has both cases? no, but regex may allow)
    # According to the doc, must contain both lowercase and uppercase, so expect False
    assert is_camel_case("A") is False

def test_boundary_conditions():
    # Leading number should invalidate
    assert is_camel_case("1CamelCase") is False
    # Only lowercase letters should invalidate
    assert is_camel_case("lowercase") is False
    # Only uppercase letters should invalidate
    assert is_camel_case("UPPERCASE") is False
    # Empty string should invalidate
    assert is_camel_case("") is False

def test_invalid_input_types():
    # Non-string input should return False, not raise
    assert is_camel_case(123) is False
    assert is_camel_case(None) is False
    assert is_camel_case(['a', 'B']) is False
