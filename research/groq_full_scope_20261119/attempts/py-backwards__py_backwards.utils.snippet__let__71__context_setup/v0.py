import builtins
import inspect
import types
import pytest

from py_backwards.utils.snippet import let, eager, get_source, VariablesGenerator


def test_let_returns_none_and_does_not_raise():
    """
    The `let` function should accept any value and return None without raising.
    """
    # Using a simple integer, string, and object to cover different types
    for value in (42, "foo", object()):
        result = let(value)
        assert result is None, f"let({value!r}) should return None, got {result!r}"


def test_get_source_returns_source_of_callable():
    """
    `get_source` should return the source code string of a given callable.
    """
    def sample_function(x, y=2):
        return x + y

    source = get_source(sample_function)
    # The source string should contain the function definition line
    assert "def sample_function" in source
    # It should also contain the body line
    assert "return x + y" in source
    # The source should be a string
    assert isinstance(source, str)


def test_eager_evaluates_callable_and_returns_result():
    """
    `eager` should evaluate a callable and return its result.
    """
    # Define a simple lambda that captures a variable from outer scope
    outer = 10
    func = lambda: outer * 3

    result = eager(func)
    assert result == 30, f"eager(lambda) should return 30, got {result}"

    # Test with a function that has side effects
    state = {"count": 0}
    def increment():
        state["count"] += 1
        return state["count"]

    result = eager(increment)
    assert result == 1
    assert state["count"] == 1
