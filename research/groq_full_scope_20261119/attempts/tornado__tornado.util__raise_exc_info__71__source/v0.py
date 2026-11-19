import pytest
import sys
import traceback
from tornado.util import raise_exc_info
from types import TracebackType
from typing import Tuple, Optional


def test_raise_exc_info_raises_original_exception():
    """raise_exc_info should raise the exception provided in exc_info."""
    exc = ValueError("test error")
    tb = exc.__traceback__
    exc_info: Tuple[Optional[type], Optional[BaseException], Optional[TracebackType]] = (
        type(exc),
        exc,
        tb,
    )
    with pytest.raises(ValueError) as excinfo:
        raise_exc_info(exc_info)
    # The raised exception should be the same instance
    assert excinfo.value is exc
    # The traceback should be preserved
    assert excinfo.value.__traceback__ is tb


def test_raise_exc_info_with_none_exception_raises_type_error():
    """If exc_info[1] is None, raise_exc_info should raise TypeError."""
    exc_info: Tuple[Optional[type], Optional[BaseException], Optional[TracebackType]] = (
        None,
        None,
        None,
    )
    with pytest.raises(TypeError) as excinfo:
        raise_exc_info(exc_info)
    assert "no exception" in str(excinfo.value)


def test_raise_exc_info_does_not_modify_input_tuple():
    """raise_exc_info should not modify the original exc_info tuple."""
    exc = RuntimeError("original")
    exc_info: Tuple[Optional[type], Optional[BaseException], Optional[TracebackType]] = (
        type(exc),
        exc,
        exc.__traceback__,
    )
    # Make a copy to compare after the call
    original_copy = exc_info
    try:
        raise_exc_info(exc_info)
    except RuntimeError:
        pass
    # The original tuple should remain unchanged
    assert exc_info == original_copy
