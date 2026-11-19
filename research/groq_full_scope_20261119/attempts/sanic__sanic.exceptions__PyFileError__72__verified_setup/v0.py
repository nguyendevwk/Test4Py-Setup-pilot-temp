import pytest
from sanic.exceptions import PyFileError


def test_pyfileerror_basic_message_and_status():
    """Verify that the error message contains the file name and default status code."""
    err = PyFileError("config.py")
    assert isinstance(err, PyFileError)
    # The message should include the file name
    assert "config.py" in str(err)
    # Default status code is None
    assert err.status_code is None
    # Default quiet flag is None
    assert err.quiet is None
    # Context, extra, headers default to None
    assert err.context is None
    assert err.extra is None
    assert err.headers is None


def test_pyfileerror_with_all_parameters():
    """Test that all optional keyword arguments are stored correctly."""
    context = {"key": "value"}
    extra = {"extra_key": 123}
    headers = {"Content-Type": "text/plain"}
    err = PyFileError(
        "settings.yaml",
        status_code=404,
        quiet=True,
        context=context,
        extra=extra,
        headers=headers,
    )
    assert err.status_code == 404
    assert err.quiet is True
    assert err.context is context
    assert err.extra is extra
    assert err.headers is headers
    # Ensure the message still contains the file name
    assert "settings.yaml" in str(err)


def test_pyfileerror_with_non_string_file():
    """Ensure that the constructor accepts any type for the file argument."""
    file_obj = object()
    err = PyFileError(file_obj)
    # The string representation should use the object's repr
    assert str(file_obj) in str(err)
    # No exception should be raised during construction
    assert isinstance(err, PyFileError)
