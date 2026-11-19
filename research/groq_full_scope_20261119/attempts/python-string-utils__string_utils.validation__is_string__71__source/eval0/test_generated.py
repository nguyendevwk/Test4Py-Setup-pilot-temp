import pytest
from string_utils.validation import is_string

def test_is_string_with_non_string(tmp_path):
    """Verify that non‑string objects return False."""
    assert is_string(123) is False
    assert is_string(b'bytes') is False
    assert is_string(['list']) is False
    assert is_string({'dict': 'value'}) is False

def test_is_string_with_empty_and_normal_strings(tmp_path):
    """Verify that empty and normal strings return True."""
    assert is_string('') is True
    assert is_string('hello') is True
    assert is_string(' ') is True
    assert is_string('\n') is True

def test_is_string_with_unicode_and_special_characters(tmp_path):
    """Verify that unicode and special characters are treated as strings."""
    assert is_string('こんにちは') is True
    assert is_string('😀') is True
    assert is_string('foo\nbar\tbaz') is True
