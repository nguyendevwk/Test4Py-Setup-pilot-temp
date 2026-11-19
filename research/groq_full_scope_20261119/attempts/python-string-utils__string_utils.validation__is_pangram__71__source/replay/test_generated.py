import string
import pytest
from string_utils.validation import is_pangram

def test_is_pangram_returns_true_for_valid_pangram():
    pangram = "The quick brown fox jumps over the lazy dog"
    assert is_pangram(pangram) is True

def test_is_pangram_returns_false_for_non_pangram():
    non_pangram = "Hello, world!"
    assert is_pangram(non_pangram) is False

def test_is_pangram_handles_non_string_input_gracefully():
    assert is_pangram(12345) is False
