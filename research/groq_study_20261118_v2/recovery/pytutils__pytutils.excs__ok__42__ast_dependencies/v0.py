import pytest
from pytutils.excs import ok


def test_ok_suppresses_specified_exception():
    """The context manager should suppress the specified exception."""
    with ok(ValueError):
        raise ValueError("suppressed")


def test_ok_reraises_unspecified_exception():
    """Exceptions not listed should propagate."""
    with pytest.raises(RuntimeError):
        with ok(ValueError):
            raise RuntimeError("not suppressed")


def test_ok_suppresses_multiple_exceptions():
    """Multiple exception types can be passed and all are suppressed."""
    with ok(ValueError, TypeError):
        raise TypeError("suppressed multiple")


def test_ok_no_exceptions_passed_reraises_any():
    """If no exception types are provided, any exception should be re-raised."""
    with pytest.raises(IndexError):
        with ok():
            raise IndexError("no types passed")


def test_ok_context_manager_returns_none():
    """The context manager should return None when used in a with statement."""
    result = ok(ValueError).__enter__()
    assert result is None
    ok(ValueError).__exit__(None, None, None)
