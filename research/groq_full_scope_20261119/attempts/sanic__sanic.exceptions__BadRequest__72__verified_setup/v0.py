import pytest
from sanic.exceptions import BadRequest


def test_default_initialization():
    """BadRequest should default to status 400, quiet True, and no message."""
    exc = BadRequest()
    assert exc.status_code == 400
    assert exc.quiet is True
    # The default message should be None, which means the default status text is used.
    assert exc.message is None
    # No context or headers should be set.
    assert getattr(exc, "context", None) is None
    assert getattr(exc, "headers", None) is None


def test_custom_message_and_headers():
    """Providing a custom message and headers should store them correctly."""
    headers = {"X-Custom": "value"}
    exc = BadRequest("Invalid input", headers=headers)
    assert exc.message == "Invalid input"
    assert exc.headers == headers
    # quiet should remain True unless explicitly overridden
    assert exc.quiet is True
    # status_code remains 400
    assert exc.status_code == 400


def test_bytes_message_and_context():
    """A bytes message should be preserved, and context should be stored as provided."""
    context = {"detail": "missing field"}
    exc = BadRequest(b"Bad bytes", context=context)
    assert isinstance(exc.message, bytes)
    assert exc.message == b"Bad bytes"
    assert exc.context == context
    # quiet default remains True
    assert exc.quiet is True
