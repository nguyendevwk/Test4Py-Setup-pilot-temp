import pytest
from string_utils.validation import is_palindrome

def test_palindrome_basic_cases():
    # Basic palindrome detection
    assert is_palindrome("LOL") is True
    assert is_palindrome("Lol") is False
    assert is_palindrome("Lol", ignore_case=True) is True
    assert is_palindrome("ROTFL") is False

def test_palindrome_with_spaces_and_case():
    # Palindrome with spaces ignored
    assert is_palindrome("i topi non avevano nipoti", ignore_spaces=True) is True
    # Same string with spaces considered should be False
    assert is_palindrome("i topi non avevano nipoti", ignore_spaces=False) is False
    # Case-insensitive palindrome
    assert is_palindrome("Madam", ignore_case=True) is True
    # Case-sensitive palindrome should be False
    assert is_palindrome("Madam", ignore_case=False) is False

def test_palindrome_boundary_and_invalid_input():
    # Empty string or only spaces should not be considered a palindrome
    assert is_palindrome("") is False
    assert is_palindrome("   ") is False
    # Non-string input should return False
    assert is_palindrome(12345) is False
    assert is_palindrome(None) is False
