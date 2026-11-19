import pytest
from py_backwards.utils.snippet import let

def test_let_returns_none_and_accepts_any_type():
    # The function should return None for any input type
    assert let(42) is None
    assert let("foo") is None
    assert let([1, 2, 3]) is None
    assert let({"a": 1}) is None

def test_let_is_idempotent_for_same_variable_name():
    # Calling let twice with the same variable name should not raise an exception
    # and should still return None each time.
    assert let("bar") is None
    assert let("bar") is None

def test_let_handles_non_string_variable_names():
    # let should accept variable names that are not strings without raising
    # (e.g., integers, tuples, etc.) and still return None.
    assert let(0) is None
    assert let((1, 2)) is None
    assert let(3.14) is None
