import pytest
from sanic.exceptions import PyFileError

def test_pyfileerror_message_includes_file():
    """PyFileError should embed the provided file name in its message."""
    exc = PyFileError("config.yaml")
    assert "config.yaml" in str(exc)
    assert exc.args[0] == "could not execute config file config.yaml"

def test_pyfileerror_with_status_and_headers():
    """PyFileError should store status_code and headers correctly."""
    headers = {"X-Custom": "value"}
    exc = PyFileError("config.yaml", status_code=404, headers=headers)
    # SanicException stores status_code in `status_code` attribute
    assert getattr(exc, "status_code", None) == 404
    # Headers are stored in `headers` attribute
    assert getattr(exc, "headers", None) == headers

def test_pyfileerror_accepts_non_string_file_and_quiet_flag():
    """PyFileError should accept any object as file and handle quiet flag."""
    obj_file = object()
    exc = PyFileError(obj_file, quiet=True)
    # The message should use the object's string representation
    assert str(obj_file) in str(exc)
    # Quiet flag should be stored in the exception
    assert getattr(exc, "quiet", None) is True
