import pytest
from string_utils.validation import is_full_string

def test_is_full_string_with_valid_and_invalid_strings():
    # Valid string with non‑space characters
    assert is_full_string("hello") is True
    # Empty string
    assert is_full_string("") is False
    # String with only whitespace
    assert is_full_string("   ") is False

def test_is_full_string_with_non_string_inputs():
    # Non‑string input should return False
    assert is_full_string(123) is False
    assert is_full_string(None) is False
    assert is_full_string([1, 2, 3]) is False

def test_is_full_string_edge_cases():
    # String with leading/trailing spaces but contains characters
    assert is_full_string("  world  ") is True
    # String with newline and tab but no visible characters
    assert is_full_string("\n\t") is False
