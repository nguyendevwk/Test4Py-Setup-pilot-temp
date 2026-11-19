import sys
import io
import pytest
from datetime import datetime
from traceback import format_exception

# Import the function under test
from thefuck.logs import exception

@pytest.fixture
def captured_stderr():
    """Capture writes to sys.stderr."""
    original_stderr = sys.stderr
    buffer = io.StringIO()
    sys.stderr = buffer
    try:
        yield buffer
    finally:
        sys.stderr = original_stderr

def test_exception_writes_formatted_output(captured_stderr):
    """Normal case: exception writes title and formatted traceback."""
    title = "TestError"
    try:
        raise ValueError("sample error")
    except Exception:
        exc_info = sys.exc_info()
    exception(title, exc_info)

    output = captured_stderr.getvalue()
    # Check that the title appears
    assert f"[WARN] {title}:" in output
    # Check that the traceback contains the exception message
    assert "ValueError: sample error" in output
    # Check that the separator line is present
    assert "----------------------------" in output

def test_exception_with_empty_title(captured_stderr):
    """Boundary case: empty title should still produce a warning header."""
    title = ""
    try:
        raise RuntimeError("empty title error")
    except Exception:
        exc_info = sys.exc_info()
    exception(title, exc_info)

    output = captured_stderr.getvalue()
    # Title is empty, but the header should still be present
    assert "[WARN] :" in output
    # Traceback should contain the exception type and message
    assert "RuntimeError: empty title error" in output

def test_exception_invalid_exc_info_raises_type_error():
    """Error case: passing invalid exc_info should raise TypeError."""
    title = "Invalid"
    # Pass a tuple that does not match the expected exc_info structure
    invalid_exc_info = ("not", "a", "tuple")
    with pytest.raises(TypeError):
        exception(title, invalid_exc_info)
