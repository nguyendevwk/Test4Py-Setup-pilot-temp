import sys
import io
import traceback
import pytest
from thefuck.logs import exception

def capture_stderr(func, *args, **kwargs):
    """Utility to capture sys.stderr output of a function."""
    old_stderr = sys.stderr
    sys.stderr = io.StringIO()
    try:
        func(*args, **kwargs)
        return sys.stderr.getvalue()
    finally:
        sys.stderr = old_stderr

def test_exception_outputs_trace_and_title():
    """The exception function should write the title and traceback to stderr."""
    exc_info = (ValueError, ValueError("boom"), None)
    output = capture_stderr(exception, "TestTitle", exc_info)
    # Title should appear in the output
    assert "TestTitle" in output
    # Traceback should contain the exception message
    assert "ValueError: boom" in output
    # The separator line should be present
    assert "----------------------------" in output

def test_exception_with_empty_title():
    """An empty title should still produce a formatted warning header."""
    exc_info = (RuntimeError, RuntimeError("oops"), None)
    output = capture_stderr(exception, "", exc_info)
    # Even with empty title, the header line should be present
    assert "WARN" in output
    # The title placeholder should be empty but not cause errors
    assert "RuntimeError: oops" in output

def test_exception_raises_on_invalid_exc_info():
    """Passing an invalid exc_info tuple should raise a TypeError."""
    with pytest.raises(TypeError):
        # exc_info must be a 3-tuple; passing a string triggers a TypeError
        exception("Invalid", "not a tuple")
