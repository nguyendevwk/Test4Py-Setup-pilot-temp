import pytest
from sanic.exceptions import SanicException
from sanic.helpers import STATUS_CODES

def test_default_initialization():
    """SanicException with no arguments should use defaults."""
    exc = SanicException()
    # Default status code is class attribute 500
    assert exc.status_code == 500
    # Default quiet is False
    assert exc.quiet is False
    # Default headers is empty dict
    assert exc.headers == {}
    # Message should be the default status text for 500
    expected_msg = STATUS_CODES.get(500, b"").decode()
    assert str(exc) == expected_msg
    # context and extra should be None
    assert exc.context is None
    assert exc.extra is None

def test_custom_status_and_headers_and_context():
    """Providing custom status, headers, context, and extra should override defaults."""
    custom_headers = {"X-Custom": "value"}
    custom_context = {"detail": "extra info"}
    custom_extra = {"internal": "secret"}
    exc = SanicException(
        "Custom error",
        status_code=418,
        headers=custom_headers,
        context=custom_context,
        extra=custom_extra,
    )
    assert exc.status_code == 418
    assert exc.headers == custom_headers
    assert exc.context == custom_context
    assert exc.extra == custom_extra
    # Message should be the one passed
    assert str(exc) == "Custom error"

def test_bytes_message_and_quiet_flag():
    """Passing a bytes message should be decoded, and quiet flag should be respected."""
    exc = SanicException(b"Byte message", quiet=True)
    # Bytes message is decoded to str
    assert str(exc) == "Byte message"
    # Quiet flag set to True
    assert exc.quiet is True
    # Default status code remains 500
    assert exc.status_code == 500
