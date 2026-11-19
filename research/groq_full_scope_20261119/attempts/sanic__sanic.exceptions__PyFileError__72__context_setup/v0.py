import pytest
from sanic.exceptions import PyFileError

def test_pyfileerror_message_and_status_code():
    """Verify that the error message includes the file name and that the status code is set correctly."""
    err = PyFileError("config.py", status_code=404)
    assert isinstance(err, PyFileError)
    assert err.status_code == 404
    # The message should contain the file name
    assert "config.py" in err.args[0]
    # The default message format is "could not execute config file <file>"
    assert err.args[0] == "could not execute config file config.py"

def test_pyfileerror_default_status_and_headers():
    """When no status code is provided, the default from SanicException should be used (500)."""
    err = PyFileError("missing.py")
    # SanicException defaults to 500
    assert err.status_code == 500
    # No custom headers passed, should be empty dict
    assert err.headers == {}

def test_pyfileerror_with_quiet_and_context():
    """Ensure that quiet flag and context dictionary are stored correctly."""
    context = {"detail": "file not found"}
    err = PyFileError("missing.py", quiet=True, context=context)
    assert err.quiet is True
    assert err.context == context
    # The message should still be formatted correctly
    assert err.args[0] == "could not execute config file missing.py"
