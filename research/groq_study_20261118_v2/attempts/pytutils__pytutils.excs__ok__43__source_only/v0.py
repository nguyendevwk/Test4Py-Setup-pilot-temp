import pytest
from contextlib import contextmanager
from pytutils.excs import ok


def test_ok_passes_specified_exception():
    """The context manager should swallow the specified exception."""
    with ok(ValueError):
        raise ValueError("expected to be swallowed")


def test_ok_reraises_other_exception():
    """Exceptions not listed should propagate."""
    with pytest.raises(TypeError):
        with ok(ValueError):
            raise TypeError("not swallowed")


def test_ok_no_exceptions_provided_raises_any():
    """If no exceptions are passed, any exception should be re-raised."""
    with pytest.raises(RuntimeError):
        with ok():
            raise RuntimeError("no exceptions passed")


def test_ok_no_exception_occurs():
    """When no exception occurs, the block should execute normally."""
    result = []
    with ok(ValueError):
        result.append(42)
    assert result == [42]


def test_ok_multiple_exceptions():
    """The context manager should swallow any of the listed exceptions."""
    with ok(ValueError, KeyError):
        raise KeyError("swallowed")
    with ok(ValueError, KeyError):
        raise ValueError("swallowed")
    # If we reach here, both exceptions were swallowed
    assert True
