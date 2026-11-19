import pytest
from sanic.exceptions import SanicException
from sanic.helpers import STATUS_CODES


def test_default_initialization():
    """SanicException with no arguments should use class defaults."""
    exc = SanicException()
    # Default status code is 500
    assert exc.status_code == 500
    # Default quiet flag is False
    assert exc.quiet is False
    # Default headers is an empty dict
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
    # Status code should be set to the provided value
    assert exc.status_code == 418
    # Quiet flag should be True
    assert exc.quiet is True
    # Headers should contain the custom header
    assert exc.headers == {"X-Custom": "value"}
    # Message should be the custom string
    assert exc.args[0] == "Custom error"
    # Context and extra should be stored
    assert exc.context == {"detail": "test"}
    assert exc.extra == {"internal": "secret"}


def test_bytes_message_and_headers():
    """Passing a bytes message should be decoded and headers defaulted correctly."""
    exc = SanicException(b"Byte message", headers={"X-Byte": "yes"})
    # Message should be decoded from bytes
    assert exc.args[0] == "Byte message"
    # Headers should be the provided dict
    assert exc.headers == {"X-Byte": "yes"}
    # Status code should default to 500
    assert exc.status_code == 500
    # Quiet flag should be False
    assert exc.quiet is False
