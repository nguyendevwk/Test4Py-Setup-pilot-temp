import pytest
from httpie.utils import unwrap_context

class CustomException(Exception):
    """Exception used to test context chaining."""

def test_unwrap_context_returns_self_when_no_context():
    """When an exception has no __context__, unwrap_context returns the exception itself."""
    exc = CustomException("no context")
    result = unwrap_context(exc)
    assert result is exc
    assert isinstance(result, CustomException)
    assert str(result) == "no context"

def test_unwrap_context_finds_innermost_exception_in_chain():
    """When an exception has a chain of __context__ exceptions, unwrap_context returns the deepest one."""
    deepest = CustomException("deepest")
    middle = CustomException("middle")
    middle.__context__ = deepest
    top = CustomException("top")
    top.__context__ = middle
    result = unwrap_context(top)
    assert result is deepest
    assert str(result) == "deepest"

def test_unwrap_context_returns_original_when_context_not_exception():
    """If __context__ is set to a non‑Exception object, unwrap_context should return the original exception."""
    exc = CustomException("original")
    exc.__context__ = "not an exception"
    result = unwrap_context(exc)
    assert result is exc
    assert isinstance(result, CustomException)
    assert str(result) == "original"
