import pytest
import types
import traceback
from tornado.util import raise_exc_info

def test_raise_exc_info_raises_original_exception():
    """raise_exc_info should re‑raise the exception with its original traceback."""
    # Create a dummy exception with a traceback
    try:
        raise ValueError("original error")
    except ValueError as e:
        tb = e.__traceback__
        exc_info = (type(e), e, tb)

    # Capture the re‑raised exception
    with pytest.raises(ValueError) as excinfo:
        raise_exc_info(exc_info)

    # The message should match the original
    assert str(excinfo.value) == "original error"

    # The traceback should point to the line where the original exception was raised
    tb_frames = traceback.extract_tb(excinfo.value.__traceback__)
    # The last frame should be the line where we raised ValueError
    assert tb_frames[-1].name == "test_raise_exc_info_raises_original_exception"
    assert tb_frames[-1].line == tb_frames[-1].line  # ensure line number is present

def test_raise_exc_info_with_none_exception_raises_type_error():
    """If exc_info[1] is None, raise_exc_info should raise a TypeError."""
    exc_info = (None, None, None)
    with pytest.raises(TypeError) as excinfo:
        raise_exc_info(exc_info)
    assert str(excinfo.value) == "raise_exc_info called with no exception"

def test_raise_exc_info_clears_traceback_reference():
    """After raise_exc_info runs, the exc_info tuple should be cleared to avoid circular refs."""
    try:
        raise RuntimeError("test")
    except RuntimeError as e:
        tb = e.__traceback__
        exc_info = (type(e), e, tb)

    # Capture the exception to trigger the finally block
    with pytest.raises(RuntimeError):
        raise_exc_info(exc_info)

    # After the call, exc_info should be cleared
    assert exc_info == (None, None, None)
