import pytest
from sanic.exceptions import SanicException
from sanic.helpers import STATUS_CODES

def test_default_initialization():
    """SanicException with no arguments should use defaults."""
    exc = SanicException()
    assert isinstance(exc, Exception)
    assert exc.status_code == 500
    assert exc.quiet is False
    assert exc.headers == {}
    # Default message should be the status code description
    expected_msg = STATUS_CODES.get(500, b"").decode()
    assert exc.args[0] == expected_msg
    assert exc.message == expected_msg
    assert exc.context is None
    assert exc.extra is None

def test_custom_status_and_headers():
    """Providing status_code and headers should override defaults."""
    custom_headers = {"X-Custom": "value"}
    exc = SanicException("Error occurred", status_code=418, headers=custom_headers)
    assert exc.status_code == 418
    assert exc.headers == custom_headers
    # Message should be the provided string
    assert exc.args[0] == "Error occurred"
    assert exc.message == "Error occurred"
    # Quiet should remain default False
    assert exc.quiet is False

def test_bytes_message_and_context():
    """Message can be bytes and context should be stored."""
    msg_bytes = b"Binary error"
    context = {"detail": "binary"}
    exc = SanicException(msg_bytes, context=context)
    # Bytes should be decoded to string
    assert exc.args[0] == "Binary error"
    assert exc.message == "Binary error"
    assert exc.context == context
    # No status_code provided, should default to 500
    assert exc.status_code == 500
