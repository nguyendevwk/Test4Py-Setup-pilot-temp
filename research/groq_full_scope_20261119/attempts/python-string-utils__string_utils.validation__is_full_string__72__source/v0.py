import pytest
from string_utils.validation import is_full_string

def test_non_string_input_returns_false():
    """Passing a non-string (e.g., None, int) should return False."""
    assert is_full_string(None) is False
    assert is_full_string(123) is False
    assert is_full_string(['a', 'b']) is False

def test_empty_or_whitespace_only_strings_return_false():
    """Empty string or string with only whitespace should return False."""
    assert is_full_string('') is False
    assert is_full_string('   ') is False
    assert is_full_string('\t\n ') is False

def test_non_empty_non_whitespace_string_returns_true():
    """A string containing at least one non-space character should return True."""
    assert is_full_string('hello') is True
    assert is_full_string('  hello  ') is True
    assert is_full_string('a') is True
