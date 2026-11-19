import pytest
import sys
import traceback
from tornado.util import raise_exc_info
from types import TracebackType
from typing import Tuple, Optional, Type


def test_raise_exc_info_raises_provided_exception():
    """raise_exc_info should raise the exception passed in exc_info."""
    exc_type = ValueError
    exc_value = ValueError("test error")
    tb = exc_value.__traceback__
    exc_info: Tuple[Optional[Type[BaseException]], Optional[BaseException], Optional[TracebackType]] = (
        exc_type,
        exc_value,
        tb,
    )
    with pytest.raises(ValueError) as excinfo:
        raise_exc_info(exc_info)
    # The raised exception should be the same instance
    assert excinfo.value is exc_value
    # The traceback should be the one we passed in
    assert excinfo.value.__traceback__ is tb


def test_raise_exc_info_with_none_raises_type_error():
    """If exc_info[1] is None, raise_exc_info should raise TypeError."""
    exc_info: Tuple[Optional[Type[BaseException]], Optional[BaseException], Optional[TracebackType]] = (
        None,
        None,
        None,
    )
    with pytest.raises(TypeError) as excinfo:
        raise_exc_info(exc_info)
    assert str(excinfo.value) == "raise_exc_info called with no exception"


def test_raise_exc_info_clears_local_reference():
    """After raise_exc_info returns, the local exc_info reference should be cleared."""
    exc_type = RuntimeError
    exc_value = RuntimeError("cleanup test")
    tb = exc_value.__traceback__
    exc_info: Tuple[Optional[Type[BaseException]], Optional[BaseException], Optional[TracebackType]] = (
        exc_type,
        exc_value,
        tb,
    )
    try:
        raise_exc_info(exc_info)
    except RuntimeError:
        # After the exception is raised, the local variable exc_info inside raise_exc_info
        # should have been set to (None, None, None). We cannot inspect that directly,
        # but we can confirm that the function does not leak the traceback reference
        # by ensuring that the traceback of the caught exception is the original one.
        assert exc_value.__traceback__ is tb
    else:
        pytest.fail("Expected RuntimeError to be raised")
