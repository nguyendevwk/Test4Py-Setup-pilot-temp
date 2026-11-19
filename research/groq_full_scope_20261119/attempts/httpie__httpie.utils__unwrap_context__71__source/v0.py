import pytest
from httpie.utils import unwrap_context

def test_unwrap_context_returns_self_when_no_context():
    """When an exception has no __context__, unwrap_context should return the exception itself."""
    exc = ValueError("simple error")
    result = unwrap_context(exc)
    assert result is exc
    assert isinstance(result, ValueError)
    assert str(result) == "simple error"

def test_unwrap_context_recurses_into_context_chain():
    """When an exception has a __context__ that is also an exception, unwrap_context should return the deepest exception."""
    # Create a chain: deepest -> middle -> outer
    deepest = KeyError("deep")
    middle = RuntimeError("middle")
    middle.__context__ = deepest
    outer = IndexError("outer")
    outer.__context__ = middle

    result = unwrap_context(outer)
    assert result is deepest
    assert isinstance(result, KeyError)
    assert str(result) == "deep"

def test_unwrap_context_returns_outer_when_context_not_exception():
    """If __context__ is not an Exception (e.g., None), unwrap_context should return the original exception."""
    exc = TypeError("type error")
    # Explicitly set __context__ to a non-Exception value
    exc.__context__ = "not an exception"
    result = unwrap_context(exc)
    assert result is exc
    assert isinstance(result, TypeError)
    assert str(result) == "type error"
