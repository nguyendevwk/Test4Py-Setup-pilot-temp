import pytest
from sanic.exceptions import URLBuildError
from sanic.helpers import STATUS_CODES


def test_urlbuilderror_default_message_and_status():
    """When no message is provided, the default status message for 500 is used."""
    exc = URLBuildError()
    assert isinstance(exc, URLBuildError)
    assert exc.status_code == 500
    # STATUS_CODES contains bytes; decode to str for comparison
    expected_msg = STATUS_CODES[500].decode()
    assert exc.args[0] == expected_msg
    assert exc.message == expected_msg
    assert exc.quiet is None  # default from SanicException
    assert exc.headers == {}  # default from SanicException


def test_urlbuilderror_bytes_message_and_context():
    """Providing a bytes message should be decoded and stored; context is preserved."""
    msg_bytes = b"Byte message"
    context = {"detail": "extra info"}
    exc = URLBuildError(msg_bytes, context=context)
    assert exc.args[0] == "Byte message"
    assert exc.message == "Byte message"
    assert exc.context == context
    # status_code should still be 500
    assert exc.status_code == 500
    # quiet and headers default
    assert exc.quiet is None
    assert exc.headers == {}


def test_urlbuilderror_custom_quiet_and_headers():
    """Custom quiet flag and headers are respected and stored."""
    headers = {"X-Custom": "value"}
    exc = URLBuildError("Custom error", quiet=True, headers=headers)
    assert exc.args[0] == "Custom error"
    assert exc.message == "Custom error"
    assert exc.quiet is True
    assert exc.headers == headers
    # context and extra default to None
    assert exc.context is None
    assert exc.extra is None
