import pytest
from string_utils.validation import is_palindrome

def test_palindrome_ignore_case_and_spaces():
    # Normal case: palindrome with mixed case and spaces, ignoring both
    s = "A man a plan a canal Panama"
    assert is_palindrome(s, ignore_spaces=True, ignore_case=True) is True
    # Same string but without ignoring spaces should be False
    assert is_palindrome(s, ignore_spaces=False, ignore_case=True) is False

def test_empty_and_non_string_inputs():
    # Boundary case: empty string should not be considered a palindrome
    assert is_palindrome("") is False
    # Non-string input should also return False
    assert is_palindrome(12345) is False
    assert is_palindrome(None) is False

def test_non_palindrome_with_case_sensitivity():
    # Error scenario: string that is not a palindrome when case matters
    assert is_palindrome("Racecar", ignore_case=False) is False
    # When case is ignored it becomes a palindrome
    assert is_palindrome("Racecar", ignore_case=True) is True
