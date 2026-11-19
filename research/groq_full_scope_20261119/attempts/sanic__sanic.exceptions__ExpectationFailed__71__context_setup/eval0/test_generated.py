import pytest
from sanic.exceptions import ExpectationFailed
from sanic.helpers import STATUS_CODES


def test_default_initialization():
    """ExpectationFailed without arguments should use status code 417 and default message."""
    exc = ExpectationFailed()
    assert isinstance(exc, ExpectationFailed)
    assert exc.status_code == 417
    # Default message should be the standard HTTP status text for 417
    expected_msg = STATUS_CODES[417].decode()
    assert exc.args[0] == expected_msg
    # quiet should be True as defined on the class
    assert exc.quiet is True
    # No headers by default
    assert exc.headers == {}


def test_custom_message_and_headers():
    """Providing a custom message and headers should override defaults."""
    custom_msg = "Custom expectation failed"
    custom_headers = {"X-Custom": "value"}
    exc = ExpectationFailed(custom_msg, headers=custom_headers)
    assert exc.status_code == 417
    assert exc.args[0] == custom_msg
    assert exc.headers == custom_headers
    # quiet remains True unless explicitly overridden
    assert exc.quiet is True


def test_bytes_message_and_context():
    """Bytes message should be decoded and context stored correctly."""
    msg_bytes = b"Bytes message"
    context = {"detail": "extra info"}
    exc = ExpectationFailed(msg_bytes, context=context)
    assert exc.args[0] == "Bytes message"
    assert exc.context == context
    # status_code and quiet should still be default
    assert exc.status_code == 417
    assert exc.quiet is True
