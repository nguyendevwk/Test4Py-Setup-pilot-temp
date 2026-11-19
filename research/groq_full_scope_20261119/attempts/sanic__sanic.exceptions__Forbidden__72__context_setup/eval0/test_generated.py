import pytest
from sanic.exceptions import Forbidden
from sanic.helpers import STATUS_CODES


def test_default_forbidden_attributes():
    """Forbidden should use default status code 403 and quiet True."""
    exc = Forbidden()
    assert exc.status_code == 403
    assert exc.quiet is True
    # Default message should be the status description
    expected_msg = STATUS_CODES[403].decode()
    assert exc.args[0] == expected_msg
    assert exc.message == expected_msg
    # No custom headers by default
    assert exc.headers == {}


def test_custom_message_and_bytes_handling():
    """Forbidden should accept string and bytes messages and decode bytes."""
    msg_str = "Access denied"
    exc_str = Forbidden(msg_str)
    assert exc_str.args[0] == msg_str
    assert exc_str.message == msg_str

    msg_bytes = b"Forbidden access"
    exc_bytes = Forbidden(msg_bytes)
    decoded = msg_bytes.decode()
    assert exc_bytes.args[0] == decoded
    assert exc_bytes.message == decoded


def test_overriding_headers_and_context():
    """Headers passed to Forbidden should override class defaults."""
    custom_headers = {"X-Custom": "value", "Content-Type": "text/plain"}
    exc = Forbidden("test", headers=custom_headers)
    assert exc.headers == custom_headers
    # Context and extra should be stored correctly
    ctx = {"user": "alice"}
    extra = {"debug": True}
    exc2 = Forbidden("msg", context=ctx, extra=extra)
    assert exc2.context == ctx
    assert exc2.extra == extra
