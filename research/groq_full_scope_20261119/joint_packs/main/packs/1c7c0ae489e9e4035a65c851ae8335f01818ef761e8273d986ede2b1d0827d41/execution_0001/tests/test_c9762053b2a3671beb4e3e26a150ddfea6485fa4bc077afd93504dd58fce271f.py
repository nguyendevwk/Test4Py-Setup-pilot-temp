import pytest
from string_utils.validation import is_palindrome

def test_simple_palindrome():
    # Normal palindrome with case sensitivity
    assert is_palindrome("madam") is True
    # Non-palindrome
    assert is_palindrome("hello") is False

def test_ignore_spaces_and_case():
    # Palindrome with spaces and mixed case
    assert is_palindrome("A man a plan a canal Panama", ignore_spaces=True, ignore_case=True) is True
    # Same string but ignoring spaces only
    assert is_palindrome("A man a plan a canal Panama", ignore_spaces=True, ignore_case=False) is False

def test_non_string_input():
    # Non-string input should return False without raising
    assert is_palindrome(12345) is False
    assert is_palindrome(None) is False
    assert is_palindrome([1, 2, 1]) is False
