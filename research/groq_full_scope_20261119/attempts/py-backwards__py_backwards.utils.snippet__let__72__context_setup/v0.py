import pytest
from py_backwards.utils.snippet import let

def test_let_returns_none_and_does_not_raise():
    """Calling let with a simple value should return None and not raise."""
    result = let(42)
    assert result is None

def test_let_accepts_string_and_returns_none():
    """Calling let with a string variable name should also return None."""
    result = let("foo")
    assert result is None

def test_multiple_calls_with_same_variable_do_not_raise():
    """Calling let multiple times with the same variable name should not raise."""
    let("bar")
    let("bar")  # should not raise an exception
    let("bar")  # repeated call
