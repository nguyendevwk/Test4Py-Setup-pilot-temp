import pytest
from contextlib import contextmanager

# Import the target function from the module under test
from pytutils.excs import ok


def test_ok_passes_without_exception():
    """The context manager should allow normal execution without raising."""
    with ok(ValueError):
        # No exception raised inside the block
        result = 1 + 1
    assert result == 2, "Result should be computed correctly when no exception occurs"


def test_ok_suppresses_specified_exception():
    """The context manager should suppress the specified exception type."""
    with ok(ValueError):
        raise ValueError("This error should be suppressed")
    # If the exception was not suppressed, the test would fail before reaching this line


def test_ok_raises_unexpected_exception():
    """The context manager should re‑raise exceptions not listed in its arguments."""
    with pytest.raises(TypeError):
        with ok(ValueError):
            raise TypeError("This error should propagate")
