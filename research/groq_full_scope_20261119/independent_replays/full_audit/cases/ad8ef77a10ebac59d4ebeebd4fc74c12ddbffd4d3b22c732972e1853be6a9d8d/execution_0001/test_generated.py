import pytest
from tornado.util import errno_from_exception


def test_errno_from_exception_with_errno_attribute():
    class CustomError(Exception):
        errno = 42

    err = CustomError("some error")
    assert errno_from_exception(err) == 42


def test_errno_from_exception_with_args_no_errno():
    err = ValueError(13, "invalid argument")
    assert errno_from_exception(err) == 13


def test_errno_from_exception_with_no_args():
    err = RuntimeError()
    assert errno_from_exception(err) is None
