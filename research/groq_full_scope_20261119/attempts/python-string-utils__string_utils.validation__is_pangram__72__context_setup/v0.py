import string
import pytest
from string_utils.validation import is_pangram

def test_is_pangram_true():
    # A classic pangram containing every letter of the alphabet
    pangram = "The quick brown fox jumps over the lazy dog"
    assert is_pangram(pangram) is True

def test_is_pangram_false():
    # A sentence missing several letters (e.g., no 'q', 'z', 'x')
    non_pangram = "Hello world, this is a test sentence."
    assert is_pangram(non_pangram) is False

def test_is_pangram_invalid_input():
    # Input that is not a non‑empty string should return False
    assert is_pangram(None) is False
    assert is_pangram("") is False
    assert is_pangram("   ") is False
