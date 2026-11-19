import sys
import io
import pytest
from contextlib import redirect_stderr
from thefuck.logs import exception
from traceback import TracebackException, format_exception

def test_exception_writes_expected_format(tmp_path):
    # Create a simple exception and capture its exc_info
    try:
        1 / 0
    except ZeroDivisionError:
        exc_info = sys.exc_info()
    # Capture stderr output
    stderr = io.StringIO()
    with redirect_stderr(stderr):
        exception("Test Title", exc_info)
    output = stderr.getvalue()
    # Assert that the title and trace are present
    assert "Test Title" in output
    assert "ZeroDivisionError" in output
    # Assert that the warning header and separator are present
    assert "WARN" in output
    assert "----------------------------" in output

def test_exception_with_custom_exception(tmp_path):
    # Use a custom exception with a message
    class MyError(Exception):
        pass
    try:
        raise MyError("custom message")
    except MyError:
        exc_info = sys.exc_info()
    stderr = io.StringIO()
    with redirect_stderr(stderr):
        exception("Custom Error", exc_info)
    output = stderr.getvalue()
    # Check that the custom message appears in the trace
    assert "custom message" in output
    # Ensure the title is correctly formatted
    assert "Custom Error" in output

def test_exception_invalid_exc_info_raises_type_error():
    # Pass an invalid exc_info tuple (missing elements)
    invalid_exc_info = (None, None)  # missing traceback
    with pytest.raises(TypeError):
        exception("Invalid", invalid_exc_info)
