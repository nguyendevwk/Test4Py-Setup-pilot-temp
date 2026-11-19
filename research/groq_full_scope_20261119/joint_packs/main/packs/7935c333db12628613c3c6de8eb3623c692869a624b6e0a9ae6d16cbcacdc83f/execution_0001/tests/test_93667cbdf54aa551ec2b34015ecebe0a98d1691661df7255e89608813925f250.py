import pytest
from tornado.util import errno_from_exception


class CustomErrnoException(Exception):
    """Exception that carries an errno attribute."""
    def __init__(self, errno: int):
        self.errno = errno
        super().__init__(f"Error {errno}")


class CustomArgsException(Exception):
    """Exception that carries errno in args but no errno attribute."""
    def __init__(self, errno: int):
        super().__init__(errno, "message")


class NoArgsException(Exception):
    """Exception with no args and no errno attribute."""
    pass


def test_errno_from_exception_with_errno_attribute():
    """When the exception has an `errno` attribute, that value is returned."""
    exc = CustomErrnoException(42)
    assert errno_from_exception(exc) == 42


def test_errno_from_exception_with_args():
    """When no `errno` attribute, the first arg is returned."""
    exc = CustomArgsException(99)
    assert errno_from_exception(exc) == 99


def test_errno_from_exception_no_errno_or_args():
    """When neither attribute nor args exist, None is returned."""
    exc = NoArgsException()
    assert errno_from_exception(exc) is None
