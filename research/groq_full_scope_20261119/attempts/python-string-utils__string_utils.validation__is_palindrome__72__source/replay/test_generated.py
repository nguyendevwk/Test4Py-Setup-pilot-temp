import pytest
from string_utils.validation import is_palindrome

def test_palindrome_basic_and_options():
    # Basic palindrome
    assert is_palindrome("otto") is True
    # Case-sensitive mismatch
    assert is_palindrome("Lol") is False
    # Case-insensitive palindrome
    assert is_palindrome("Lol", ignore_case=True) is True
    # Spaces ignored
    assert is_palindrome("i topi non avevano nipoti", ignore_spaces=True) is True
    # Spaces matter
    assert is_palindrome("i topi non avevano nipoti", ignore_spaces=False) is False

def test_boundary_empty_and_single_character():
    # Empty string is not considered a full string, should return False
    assert is_palindrome("") is False
    # Single character is a palindrome
    assert is_palindrome("a") is True

def test_error_non_string_input():
    # Non-string input should be treated as not a full string and return False
    assert is_palindrome(12345) is False
    assert is_palindrome(None) is False
