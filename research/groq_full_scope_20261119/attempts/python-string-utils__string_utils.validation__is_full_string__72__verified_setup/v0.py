import pytest
from string_utils.validation import is_full_string

def test_non_string_inputs_return_false():
    """Passing non-string values should return False."""
    assert is_full_string(123) is False
    assert is_full_string([1, 2, 3]) is False
    assert is_full_string({'key': 'value'}) is False
    assert is_full_string(None) is False

def test_strings_with_only_whitespace_return_false():
    """Strings that contain only whitespace should return False."""
    assert is_full_string('') is False
    assert is_full_string('   ') is False
    assert is_full_string('\t\n') is False

def test_valid_non_empty_strings_return_true():
    """Non-empty strings containing at least one non-space character should return True."""
    assert is_full_string('hello') is True
    assert is_full_string('  hello  ') is True
    assert is_full_string('a') is True
