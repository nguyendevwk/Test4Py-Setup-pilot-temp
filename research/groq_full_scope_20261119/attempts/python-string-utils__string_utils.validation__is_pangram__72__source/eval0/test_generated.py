import string
import pytest
from string_utils.validation import is_pangram

def test_is_pangram_with_valid_pangram():
    # Classic pangram with mixed case and punctuation
    pangram = "The quick brown fox jumps over the lazy dog!"
    assert is_pangram(pangram) is True

def test_is_pangram_boundary_empty_and_nonstring():
    # Empty string should not be a pangram
    assert is_pangram("") is False
    # Non-string input should also return False
    assert is_pangram(12345) is False

def test_is_pangram_with_missing_letters():
    # A string missing at least one letter of the alphabet
    incomplete = "abcdefghijklmnopqrstuvwxyz"[:25]  # missing 'y' and 'z'
    assert is_pangram(incomplete) is False
