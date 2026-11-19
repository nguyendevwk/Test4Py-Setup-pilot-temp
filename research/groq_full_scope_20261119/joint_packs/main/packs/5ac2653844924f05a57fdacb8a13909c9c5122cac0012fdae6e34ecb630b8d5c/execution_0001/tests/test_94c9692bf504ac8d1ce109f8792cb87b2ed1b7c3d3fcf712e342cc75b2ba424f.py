import string
import pytest
from string_utils.validation import is_pangram

def test_pangram_with_mixed_case_and_spaces():
    # A classic pangram with mixed case and spaces
    pangram = "The quick brown fox jumps over the lazy dog"
    assert is_pangram(pangram) is True

def test_non_pangram_missing_letters():
    # Missing letter 'q' and 'z'
    non_pangram = "Hello world, this is a test sentence."
    assert is_pangram(non_pangram) is False

def test_non_string_input_returns_false():
    # Passing an integer should not raise an exception but return False
    assert is_pangram(12345) is False
