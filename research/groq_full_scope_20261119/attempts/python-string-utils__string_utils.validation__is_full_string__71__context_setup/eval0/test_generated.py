import pytest
from string_utils.validation import is_full_string

def test_is_full_string_normal_cases():
    # Normal strings that should return True
    assert is_full_string("hello") is True
    assert is_full_string("  hello  ") is True
    assert is_full_string("a") is True
    # Strings that are empty or only whitespace should return False
    assert is_full_string("") is False
    assert is_full_string("   ") is False
    # Non-string inputs should return False
    assert is_full_string(123) is False
    assert is_full_string(None) is False

def test_is_full_string_boundary_cases():
    # Boundary: string with a single space character
    assert is_full_string(" ") is False
    # Boundary: string with a single non-space character
    assert is_full_string("x") is True
    # Boundary: string with leading/trailing spaces but contains a character
    assert is_full_string("  x  ") is True

def test_is_full_string_error_behavior():
    # Passing an object that is not a string should not raise an exception
    # but should return False
    class Dummy: pass
    dummy = Dummy()
    assert is_full_string(dummy) is False
    # Passing a bytes object should return False
    assert is_full_string(b"bytes") is False
