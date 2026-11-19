import pytest
from sanic.exceptions import Forbidden
from sanic.helpers import STATUS_CODES


def test_default_forbidden_attributes():
    """Forbidden should default to status 403, quiet True, and use status text as message."""
    exc = Forbidden()
    assert exc.status_code == 403
    assert exc.quiet is True
    # Default message should be the status text for 403
    expected_msg = STATUS_CODES[403].decode()
    assert exc.message == expected_msg
    assert exc.headers == {}


def test_forbidden_with_bytes_message_and_custom_headers():
    """Forbidden should decode bytes messages and allow custom headers."""
    custom_headers = {"X-Custom": "value"}
    exc = Forbidden(b"Forbidden access", headers=custom_headers)
    assert exc.message == "Forbidden access"
    assert exc.headers == custom_headers
    # status_code remains default
    assert exc.status_code == 403
    # quiet remains default True
    assert exc.quiet is True


def test_forbidden_context_and_extra():
    """Forbidden should store context and extra data correctly."""
    ctx = {"user": "alice"}
    extra = {"debug": "info"}
    exc = Forbidden("Access denied", context=ctx, extra=extra)
    assert exc.context == ctx
    assert exc.extra == extra
    assert exc.message == "Access denied"
    # status_code default
    assert exc.status_code == 403
    # quiet default True
    assert exc.quiet is True
