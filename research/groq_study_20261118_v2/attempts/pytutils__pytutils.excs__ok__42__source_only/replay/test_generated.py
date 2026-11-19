import pytest
from contextlib import contextmanager
from pytutils.excs import ok


def test_ok_passes_specified_exception():
    """The context manager should swallow the specified exception."""
    with ok(ValueError):
        raise ValueError("expected to be swallowed")


def test_ok_reraises_unspecified_exception():
    """The context manager should re‑raise exceptions that are not specified."""
    with pytest.raises(RuntimeError):
        with ok(ValueError):
            raise RuntimeError("not specified")


def test_ok_passes_multiple_exceptions():
    """Multiple exception types can be passed and any of them will be swallowed."""
    with ok(ValueError, KeyError):
        raise KeyError("one of the allowed types")


def test_ok_no_exceptions_specified_raises_all():
    """If no exception types are provided, all exceptions are re‑raised."""
    with pytest.raises(IndexError):
        with ok():
            raise IndexError("no types specified")


def test_ok_context_manager_no_exception():
    """When no exception occurs, the context manager should behave normally."""
    with ok(ValueError):
        x = 1 + 1
    assert x == 2


def test_ok_nested_contexts():
    """Nested ok contexts should each handle their own exception types."""
    with ok(ValueError):
        with ok(KeyError):
            raise KeyError("inner")
        # outer should not swallow KeyError
    with pytest.raises(KeyError):
        with ok(ValueError):
            raise KeyError("outer")


def test_ok_exception_subclass_handling():
    """Subclass of a specified exception should also be swallowed."""
    class MyError(ValueError):
        pass

    with ok(ValueError):
        raise MyError("subclass should be swallowed")


def test_ok_exception_subclass_not_handled():
    """Subclass of an unspecified exception should still be re‑raised."""
    class MyError(RuntimeError):
        pass

    with pytest.raises(MyError):
        with ok(ValueError):
            raise MyError("subclass not handled")
