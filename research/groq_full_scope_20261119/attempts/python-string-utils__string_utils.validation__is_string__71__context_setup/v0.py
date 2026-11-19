import pytest
from string_utils.validation import is_string

def test_is_string_with_regular_string():
    """Normal case: a typical string should return True."""
    assert is_string("hello world") is True

def test_is_string_with_non_string_and_empty():
    """Boundary cases: empty string is still a string, but other types are not."""
    assert is_string("") is True          # empty string is a valid string
    assert is_string(123) is False        # integer is not a string
    assert is_string(b"bytes") is False   # bytes are not str

def test_is_string_with_none_and_custom_object():
    """Error-like inputs: None and a custom object should return False."""
    class Dummy: pass
    assert is_string(None) is False
    assert is_string(Dummy()) is False
