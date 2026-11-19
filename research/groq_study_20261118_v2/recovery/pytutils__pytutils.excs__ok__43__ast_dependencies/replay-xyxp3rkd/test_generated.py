import pytest
from contextlib import contextmanager
from pytutils.excs import ok


def test_ok_passes_expected_exception():
    """The context manager should swallow the specified exception."""
    with ok(ValueError):
        raise ValueError("expected error")


def test_ok_rethrows_unexpected_exception():
    """The context manager should re‑raise exceptions not listed."""
    with pytest.raises(RuntimeError):
        with ok(ValueError):
            raise RuntimeError("unexpected error")


def test_ok_accepts_multiple_exceptions():
    """Multiple exception types can be passed and any of them will be swallowed."""
    with ok(ValueError, KeyError):
        raise KeyError("key error")
    with ok(ValueError, KeyError):
        raise ValueError("value error")


def test_ok_no_exceptions_passed():
    """If no exception types are provided, all exceptions should be re‑raised."""
    with pytest.raises(IndexError):
        with ok():
            raise IndexError("index error")


def test_ok_context_manager_no_exception():
    """If no exception is raised, the context manager should behave normally."""
    with ok(ValueError):
        x = 1 + 1
    assert x == 2
