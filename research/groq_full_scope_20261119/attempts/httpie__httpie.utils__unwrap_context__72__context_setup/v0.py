import pytest
from httpie.utils import unwrap_context


def test_unwrap_context_returns_self_when_no_context():
    """When an exception has no __context__, unwrap_context should return the exception itself."""
    exc = ValueError("simple error")
    result = unwrap_context(exc)
    assert result is exc
    assert isinstance(result, ValueError)
    assert str(result) == "simple error"


def test_unwrap_context_recurses_into_nested_context():
    """When an exception has a __context__ that is also an exception, unwrap_context should return the deepest one."""
    # Create a chain: deepest -> middle -> top
    deepest = KeyError("deep")
    middle = RuntimeError("middle")
    middle.__context__ = deepest
    top = IndexError("top")
    top.__context__ = middle

    result = unwrap_context(top)
    assert result is deepest
    assert isinstance(result, KeyError)
    assert str(result) == "deep"


def test_unwrap_context_stops_when_context_not_exception():
    """If __context__ is not an Exception instance, unwrap_context should stop and return the original exception."""
    class Dummy:
        pass

    exc = ValueError("error")
    exc.__context__ = Dummy()  # non‑Exception context
    result = unwrap_context(exc)
    assert result is exc
    assert isinstance(result, ValueError)
    assert str(result) == "error"
