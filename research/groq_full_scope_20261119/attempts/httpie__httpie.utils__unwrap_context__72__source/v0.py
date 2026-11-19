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
    """When an exception has a __context__ that is another exception, unwrap_context should return the deepest one."""
    try:
        try:
            raise KeyError("inner")
        except KeyError as inner:
            raise ValueError("outer") from inner
    except ValueError as outer:
        result = unwrap_context(outer)
        # The deepest exception is the KeyError
        assert isinstance(result, KeyError)
        assert str(result) == "inner"
        # The outer exception should not be returned
        assert result is not outer


def test_unwrap_context_handles_non_exception_context():
    """If __context__ is not an Exception instance, unwrap_context should return the original exception."""
    class Dummy:
        pass

    exc = RuntimeError("error")
    # Manually set a non-exception context
    exc.__context__ = Dummy()
    result = unwrap_context(exc)
    assert result is exc
    assert isinstance(result, RuntimeError)
    assert str(result) == "error"
