import pytest
from string_utils.validation import is_palindrome

def test_simple_palindrome():
    """A basic palindrome should return True."""
    assert is_palindrome("radar") is True
    assert is_palindrome("radar") == True

def test_ignore_spaces_and_case():
    """When ignoring spaces and case, a sentence becomes a palindrome."""
    sentence = "A man a plan a canal Panama"
    # Without ignoring spaces or case, it should be False
    assert is_palindrome(sentence) is False
    # Ignoring spaces and case should make it True
    assert is_palindrome(sentence, ignore_spaces=True, ignore_case=True) is True

def test_non_string_input_returns_false():
    """Non-string inputs should be treated as non-palindromes."""
    assert is_palindrome(12321) is False
    assert is_palindrome(None) is False
    assert is_palindrome(["a", "b", "a"]) is False
