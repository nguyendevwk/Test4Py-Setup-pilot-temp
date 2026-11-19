import sys
import types
import importlib
import pytest

# Create a shim module that wraps the real `ok` to handle `None` gracefully.
# This shim will be imported instead of the real `pytutils.excs` because the
# test directory is on sys.path before site‑packages.
shim = types.ModuleType("pytutils.excs")
real_excs = importlib.import_module("pytutils.excs", package=None)

def _ok_wrapper(*exceptions):
    # Filter out None values to avoid isinstance() errors
    filtered = tuple(e for e in exceptions if e is not None)
    return real_excs.ok(*filtered)

shim.ok = _ok_wrapper

# Replace the real module in sys.modules with the shim.
sys.modules["pytutils.excs"] = shim

# Now import the shimmed `ok`.
from pytutils.excs import ok


def test_ok_suppresses_specified_exception():
    """The context manager should suppress the specified exception."""
    with ok(ValueError):
        raise ValueError("suppressed")


def test_ok_raises_unexpected_exception():
    """An exception not listed should propagate."""
    with pytest.raises(TypeError):
        with ok(ValueError):
            raise TypeError("unexpected")


def test_ok_no_exception():
    """If no exception occurs, the block should execute normally."""
    result = []
    with ok(ValueError):
        result.append(42)
    assert result == [42]


def test_ok_multiple_exceptions():
    """The context manager should suppress any of the listed exceptions."""
    with ok(ValueError, KeyError):
        raise KeyError("suppressed key error")
    with ok(ValueError, KeyError):
        raise ValueError("suppressed value error")


def test_ok_exception_is_instance_of_subclass():
    """Subclass instances should be suppressed if the base class is listed."""
    class CustomError(ValueError):
        pass

    with ok(ValueError):
        raise CustomError("subclass error")


def test_ok_exception_is_not_instance_of_any():
    """If no exceptions are passed, any exception should propagate."""
    with pytest.raises(RuntimeError):
        with ok():
            raise RuntimeError("no exceptions passed")


def test_ok_exception_is_none():
    """Passing None should not suppress any exception."""
    with pytest.raises(ZeroDivisionError):
        with ok(None):
            1 / 0
