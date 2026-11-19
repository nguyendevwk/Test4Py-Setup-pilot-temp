import pytest
from sanic.exceptions import PyFileError
from sanic.helpers import STATUS_CODES


def test_pyfileerror_message_and_status_code():
    """PyFileError should format its message with the provided file name
    and use the supplied status code."""
    exc = PyFileError("config.py", status_code=404)
    assert str(exc) == "could not execute config file config.py"
    assert exc.status_code == 404
    # The message attribute should match the string representation
    assert exc.message == "could not execute config file config.py"


def test_pyfileerror_default_status_and_headers():
    """When no status code is provided, PyFileError should default to 500
    and inherit default headers from SanicException."""
    exc = PyFileError("missing.py")
    assert exc.status_code == 500
    # Default headers are an empty dict
    assert exc.headers == {}
    # The message should still contain the file name
    assert "missing.py" in str(exc)


def test_pyfileerror_custom_context_and_quiet():
    """PyFileError should accept custom context and quiet flags
    and expose them correctly."""
    context = {"detail": "file not found"}
    exc = PyFileError("bad.py", quiet=True, context=context)
    assert exc.quiet is True
    assert exc.context == context
    # The status code should still be the default 500
    assert exc.status_code == 500
    # The message should be correctly formatted
    assert exc.message == "could not execute config file bad.py"
