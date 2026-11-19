import pytest
from tornado.util import errno_from_exception


def test_errno_from_exception_with_errno_attribute():
    """When the exception has an `errno` attribute, it should be returned."""
    class CustomError(Exception):
        errno = 42

    err = CustomError("something went wrong")
    assert errno_from_exception(err) == 42


def test_errno_from_exception_with_args_only():
    """When the exception has no `errno` attribute but has args, the first arg should be returned."""
    err = ValueError(13, "invalid value")
    assert errno_from_exception(err) == 13


def test_errno_from_exception_no_errno_no_args():
    """When the exception has neither `errno` nor args, None should be returned."""
    err = Exception()
    assert errno_from_exception(err) is None
