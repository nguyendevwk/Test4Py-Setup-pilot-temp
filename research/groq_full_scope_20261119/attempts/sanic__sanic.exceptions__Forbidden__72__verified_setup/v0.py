import pytest
from sanic.exceptions import Forbidden
from sanic.exceptions import HTTPException


def test_forbidden_default_attributes():
    """Forbidden should default to status 403 and quiet=True."""
    exc = Forbidden()
    assert isinstance(exc, HTTPException)
    assert exc.status_code == 403
    # quiet defaults to True as defined on the class
    assert exc.quiet is True
    # message defaults to None
    assert exc.message is None
    # context and extra default to None
    assert exc.context is None
    assert exc.extra is None
    # headers default to None
    assert exc.headers is None


def test_forbidden_with_message_and_headers():
    """Providing a message and custom headers should store them correctly."""
    custom_headers = {"X-Custom": "value"}
    exc = Forbidden("Access denied", headers=custom_headers)
    assert exc.message == "Access denied"
    assert exc.headers == custom_headers
    # quiet remains True unless overridden
    assert exc.quiet is True
    # context and extra remain None
    assert exc.context is None
    assert exc.extra is None


def test_forbidden_context_and_extra():
    """Context and extra data should be stored and accessible."""
    ctx = {"user": "alice", "action": "delete"}
    extra = {"debug": "info"}
    exc = Forbidden("Forbidden", context=ctx, extra=extra)
    assert exc.context == ctx
    assert exc.extra == extra
    # message and headers default to None
    assert exc.message == "Forbidden"
    assert exc.headers is None
