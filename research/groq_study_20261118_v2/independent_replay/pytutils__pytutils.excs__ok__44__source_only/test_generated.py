import pytest
from pytutils.excs import ok


def test_ok_passes_specified_exception():
    """The context manager should swallow the specified exception."""
    with ok(ValueError):
        raise ValueError("expected to be swallowed")


def test_ok_reraises_unspecified_exception():
    """The context manager should re‑raise exceptions not listed."""
    with pytest.raises(TypeError):
        with ok(ValueError):
            raise TypeError("not swallowed")


def test_ok_no_exception():
    """No exception should propagate when nothing is raised."""
    with ok(ValueError):
        x = 1 + 1
    assert x == 2


def test_ok_multiple_exceptions():
    """Multiple exception types can be passed and all are swallowed."""
    with ok(ValueError, KeyError):
        raise KeyError("swallowed")
    with ok(ValueError, KeyError):
        raise ValueError("swallowed")
    # Ensure other exception still propagates
    with pytest.raises(IndexError):
        with ok(ValueError, KeyError):
            raise IndexError("not swallowed")


def test_ok_empty_tuple():
    """Passing no exceptions should behave like a normal context manager."""
    with pytest.raises(RuntimeError):
        with ok():
            raise RuntimeError("no exceptions specified")
