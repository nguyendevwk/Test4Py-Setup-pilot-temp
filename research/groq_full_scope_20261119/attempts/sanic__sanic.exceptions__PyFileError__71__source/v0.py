import pytest
from sanic.exceptions import PyFileError


def test_pyfileerror_basic_message_and_status():
    """PyFileError should format its message with the given file name
    and expose the provided status code."""
    err = PyFileError("config.py", status_code=404)
    assert str(err) == "could not execute config file config.py"
    assert err.status_code == 404
    # SanicException stores quiet, context, extra, headers as attributes
    assert err.quiet is None
    assert err.context is None
    assert err.extra is None
    assert err.headers is None


def test_pyfileerror_with_all_optional_kwargs():
    """All optional keyword arguments should be stored correctly."""
    err = PyFileError(
        "/etc/sanic/config.py",
        quiet=True,
        context={"user": "admin"},
        extra={"debug": True},
        headers={"X-Custom": "value"},
    )
    assert str(err) == "could not execute config file /etc/sanic/config.py"
    assert err.quiet is True
    assert err.context == {"user": "admin"}
    assert err.extra == {"debug": True}
    assert err.headers == {"X-Custom": "value"}


def test_pyfileerror_message_with_non_string_file():
    """The file argument can be any object; its string representation
    should appear in the error message."""
    class Dummy:
        def __str__(self):
            return "dummy_config.py"

    dummy_file = Dummy()
    err = PyFileError(dummy_file)
    assert str(err) == "could not execute config file dummy_config.py"
    # Ensure that the original object is still accessible via the message
    assert "dummy_config.py" in str(err)
