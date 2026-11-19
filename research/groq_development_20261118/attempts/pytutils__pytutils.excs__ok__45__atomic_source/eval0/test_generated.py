import pytest
from contextlib import contextmanager

# Import the target function from the production code
from pytutils.excs import ok


def test_ok_passes_no_exception():
    """When no exception is raised inside the context, execution continues normally."""
    with ok(ValueError):
        # No exception should be raised here
        result = 1 + 1
    assert result == 2, "The context should not alter normal execution"


def test_ok_suppresses_specified_exception():
    """When an exception of the specified type is raised, it is suppressed."""
    with ok(ValueError):
        raise ValueError("This should be suppressed")
    # If the exception was not suppressed, the test would fail before reaching this line


def test_ok_raises_unexpected_exception():
    """When an exception of an unexpected type is raised, it propagates."""
    with pytest.raises(TypeError):
        with ok(ValueError):
            raise TypeError("Unexpected exception")
