import pytest
from contextlib import contextmanager

# Import the target function from the module under test
from pytutils.excs import ok


def test_ok_passes_specified_exception():
    """When the specified exception is raised inside the context, it should be suppressed."""
    with ok(ValueError):
        raise ValueError("expected suppression")
    # If no exception propagates, the test passes


def test_ok_rethrows_unspecified_exception():
    """When an unexpected exception type is raised, it should propagate."""
    with pytest.raises(RuntimeError):
        with ok(ValueError):
            raise RuntimeError("unexpected exception")


def test_ok_no_exception():
    """When no exception is raised, the context manager should behave normally."""
    with ok(ValueError):
        x = 1 + 1
    assert x == 2
