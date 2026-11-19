import pytest
from sanic.exceptions import SanicException
from sanic.helpers import STATUS_CODES


def test_default_initialization():
    """SanicException with no arguments should use defaults."""
    exc = SanicException()
    # Default status code is class attribute 500
    assert exc.status_code == 500
    # Default quiet flag is class attribute False
    assert exc.quiet is False
    # Default headers is empty dict
    assert exc.headers == {}
    # Message should be the default status message for 500
    assert exc.args[0] == STATUS_CODES[500].decode()
    # context and extra should be None
    assert exc.context is None
    assert exc.extra is None


def test_custom_message_and_status():
    """Providing a custom message and status code should override defaults."""
    exc = SanicException(
        "Custom error",
        status_code=418,
        quiet=True,
        context={"detail": "test"},
        extra={"internal": "secret"},
        headers={"X-Custom": "value"},
    )
    assert exc.status_code == 418
    assert exc.quiet is True
    assert exc.headers == {"X-Custom": "value"}
    assert exc.args[0] == "Custom error"
    assert exc.context == {"detail": "test"}
    assert exc.extra == {"internal": "secret"}


def test_bytes_message_and_headers():
    """Message can be bytes and headers default to class attribute if not provided."""
    class CustomException(SanicException):
        status_code = 404
        headers = {"X-Default": "yes"}

    # Bytes message should be decoded
    exc = CustomException(b"Not Found")
    assert exc.args[0] == "Not Found"
    # Status code from class attribute
    assert exc.status_code == 404
    # Headers from class attribute
    assert exc.headers == {"X-Default": "yes"}
    # Quiet should be default False
    assert exc.quiet is False
