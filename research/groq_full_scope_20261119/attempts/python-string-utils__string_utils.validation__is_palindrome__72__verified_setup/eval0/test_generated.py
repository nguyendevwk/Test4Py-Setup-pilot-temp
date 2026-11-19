import pytest
from string_utils.validation import is_palindrome

def test_simple_palindrome():
    # A simple palindrome with identical case
    assert is_palindrome("racecar") is True
    # Non-palindrome
    assert is_palindrome("hello") is False

def test_ignore_spaces_and_case():
    # Palindrome with spaces and mixed case
    mixed = "A man a plan a canal Panama"
    # Without ignoring spaces or case, should be False
    assert is_palindrome(mixed) is False
    # Ignoring spaces but not case still False
    assert is_palindrome(mixed, ignore_spaces=True) is False
    # Ignoring case but not spaces still False
    assert is_palindrome(mixed, ignore_case=True) is False
    # Ignoring both spaces and case should be True
    assert is_palindrome(mixed, ignore_spaces=True, ignore_case=True) is True

def test_non_string_input_returns_false():
    # Input that is not a string should return False
    assert is_palindrome(12345) is False
    assert is_palindrome(None) is False
    assert is_palindrome([1, 2, 1]) is False
