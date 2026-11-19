import pytest
from sanic.exceptions import SanicException
from sanic.helpers import STATUS_CODES


def test_default_initialization():
    """SanicException with no arguments should use defaults."""
    exc = SanicException()
    # Default status code is class attribute 500
    assert exc.status_code == 500
    # Default quiet flag is False
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
    exc = SanicException("Custom error", status_code=418, quiet=True, headers={"X-Test": "value"})
    # Status code should be the provided one
    assert exc.status_code == 418
    # Quiet flag should be True
    assert exc.quiet is True
    # Headers should contain the custom header
    assert exc.headers == {"X-Test": "value"}
    # Message should be the custom message
    assert exc.args[0] == "Custom error"
    # context and extra remain None
    assert exc.context is None
    assert exc.extra is None


def test_bytes_message_and_headers():
    """Bytes message should be decoded and headers default to class attribute."""
    # Define a subclass with custom default headers
    class CustomException(SanicException):
        headers = {"X-Default": "yes"}

    # Pass a bytes message
    exc = CustomException(b"Byte message", status_code=404)
    # Message should be decoded
    assert exc.args[0] == "Byte message"
    # Status code should be 404
    assert exc.status_code == 404
    # Headers should be the subclass default
    assert exc.headers == {"X-Default": "yes"}
    # Quiet should be default False
    assert exc.quiet is False
