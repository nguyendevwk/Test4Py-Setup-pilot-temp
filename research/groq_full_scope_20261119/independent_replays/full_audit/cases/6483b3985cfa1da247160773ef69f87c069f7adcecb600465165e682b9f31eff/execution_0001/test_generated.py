import string
import pytest
from string_utils.validation import is_pangram

def test_is_pangram_true():
    """A classic pangram should return True."""
    pangram = "The quick brown fox jumps over the lazy dog"
    assert is_pangram(pangram) is True

def test_is_pangram_false_on_missing_letters():
    """A string missing letters should return False."""
    incomplete = "The quick brown fox jumps over the lazy do"  # missing 'g'
    assert is_pangram(incomplete) is False

def test_is_pangram_false_on_non_string_input():
    """Non‑string inputs should be treated as non‑pangrams."""
    assert is_pangram(12345) is False
    assert is_pangram(None) is False
    assert is_pangram("") is False
