import pytest
import types
import sys
from tornado.util import raise_exc_info

def test_raise_exc_info_with_traceback():
    # Create a dummy exception and capture its traceback
    try:
        raise ValueError("test error")
    except ValueError as e:
        tb = e.__traceback__
        exc_info = (type(e), e, tb)

    # The function should re‑raise the same exception with the original traceback
    with pytest.raises(ValueError) as excinfo:
        raise_exc_info(exc_info)

    # Verify that the exception message matches
    assert str(excinfo.value) == "test error"
    # Verify that the traceback points to the line where the original exception was raised
    assert excinfo.traceback.tb_lineno == excinfo.traceback.tb_frame.f_lineno - 2

def test_raise_exc_info_without_traceback():
    # Create an exception without an explicit traceback
    exc = RuntimeError("no traceback")
    exc_info = (type(exc), exc, None)

    with pytest.raises(RuntimeError) as excinfo:
        raise_exc_info(exc_info)

    assert str(excinfo.value) == "no traceback"
    # The traceback should be the current frame where raise_exc_info was called
    assert excinfo.traceback.tb_frame.f_code.co_name == "raise_exc_info"

def test_raise_exc_info_no_exception_raises_type_error():
    # Pass an exc_info tuple with None as the exception instance
    exc_info = (None, None, None)

    with pytest.raises(TypeError) as excinfo:
        raise_exc_info(exc_info)

    assert str(excinfo.value) == "raise_exc_info called with no exception"
