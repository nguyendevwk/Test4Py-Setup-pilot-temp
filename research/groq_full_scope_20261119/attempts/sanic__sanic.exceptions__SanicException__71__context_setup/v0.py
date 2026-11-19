import pytest
from sanic.exceptions import SanicException
from sanic.helpers import STATUS_CODES


def test_default_initialization():
    """SanicException with no arguments should use defaults."""
    exc = SanicException()
    # default status code is 500
    assert exc.status_code == 500
    # default quiet flag is False
    assert exc.quiet is False
    # default headers is empty dict
    assert exc.headers == {}
    # message should be the default status message for 500
    assert exc.args[0] == STATUS_CODES[500].decode()
    # context and extra should be None
    assert exc.context is None
    assert exc.extra is None


def test_custom_message_and_headers():
    """Providing a bytes message and custom headers should be handled correctly."""
    custom_headers = {"X-Custom": "value"}
    exc = SanicException(
        message=b"Custom error",
        status_code=418,
        headers=custom_headers,
        quiet=True,
        context={"detail": "test"},
        extra={"internal": "secret"},
    )
    # message should be decoded from bytes
    assert exc.args[0] == "Custom error"
    # status code should be set to 418
    assert exc.status_code == 418
    # quiet flag should be True
    assert exc.quiet is True
    # headers should match the provided dict
    assert exc.headers == custom_headers
    # context and extra should be stored
    assert exc.context == {"detail": "test"}
    assert exc.extra == {"internal": "secret"}


def test_status_code_without_message():
    """If message is None and status_code is provided, message should be derived from STATUS_CODES."""
    exc = SanicException(status_code=404)
    # message should be the status text for 404
    assert exc.args[0] == STATUS_CODES[404].decode()
    # status code should be 404
    assert exc.status_code == 404
    # quiet should default to False
    assert exc.quiet is False
