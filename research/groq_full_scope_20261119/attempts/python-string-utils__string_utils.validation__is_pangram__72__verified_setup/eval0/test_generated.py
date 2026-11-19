import string
import pytest
from string_utils.validation import is_pangram

def test_pangram_true():
    """A classic pangram should return True."""
    pangram = "The quick brown fox jumps over the lazy dog"
    assert is_pangram(pangram) is True

def test_pangram_false_missing_letters():
    """A string missing letters should return False."""
    incomplete = "The quick brown fox jumps over the lazy do"
    assert is_pangram(incomplete) is False

def test_pangram_invalid_input_type():
    """Non-string input should be treated as not a full string and return False."""
    assert is_pangram(12345) is False
