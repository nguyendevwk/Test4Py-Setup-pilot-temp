import pytest
from py_backwards.utils.snippet import let

def test_let_returns_none():
    """`let` should return None regardless of the input."""
    result = let("x")
    assert result is None

def test_let_accepts_string_variable_name():
    """`let` should accept a string representing a variable name without raising."""
    try:
        let("my_var")
    except Exception as exc:
        pytest.fail(f"let raised an unexpected exception: {exc}")

def test_let_accepts_non_string_input():
    """`let` should accept non-string inputs (e.g., integers) without raising."""
    try:
        let(42)
    except Exception as exc:
        pytest.fail(f"let raised an unexpected exception with non-string input: {exc}")
