import pytest
from sanic.exceptions import Forbidden


def test_forbidden_default_attributes():
    """Forbidden should default to status 403 and quiet=True."""
    exc = Forbidden()
    assert isinstance(exc, Forbidden)
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
    headers = {"X-Custom": "value"}
    exc = Forbidden("Access denied", headers=headers)
    assert exc.message == "Access denied"
    assert exc.headers == headers
    # quiet remains True unless explicitly overridden
    assert exc.quiet is True
    # status_code remains unchanged
    assert exc.status_code == 403


def test_forbidden_context_and_extra():
    """Context and extra mappings should be preserved on the exception."""
    context = {"user_id": 42}
    extra = {"debug": "info"}
    exc = Forbidden("Forbidden", context=context, extra=extra)
    assert exc.context == context
    assert exc.extra == extra
    # Ensure that context and extra are distinct objects
    assert exc.context is not exc.extra
    # Changing the original dicts should not affect the stored ones
    context["user_id"] = 99
    assert exc.context["user_id"] == 42
