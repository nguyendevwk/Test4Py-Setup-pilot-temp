import pytest
from contextlib import contextmanager

# Import the target function from the package
from pytutils.excs import ok


def test_ok_passes_when_no_exception():
    """The context manager should allow normal execution without raising."""
    with ok(ValueError):
        # No exception raised inside the block
        result = 1 + 1
    assert result == 2


def test_ok_suppresses_specified_exception():
    """The context manager should suppress the specified exception type."""
    with ok(ValueError):
        raise ValueError("expected error")
    # If the exception was not suppressed, the test would fail before reaching this line


def test_ok_rethrows_unspecified_exception():
    """The context manager should re‑raise exceptions not listed in its arguments."""
    with pytest.raises(RuntimeError):
        with ok(ValueError):
            raise RuntimeError("unexpected error")
