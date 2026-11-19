import pytest
from sanic.exceptions import Forbidden
from sanic.helpers import STATUS_CODES


def test_forbidden_default_attributes():
    """Forbidden should default to status 403 and quiet True."""
    exc = Forbidden()
    assert exc.status_code == 403
    assert exc.quiet is True
    # The default message should be None, which means the exception will use the status text
    assert exc.message is None
    # The default status text should match the standard status code description
    assert STATUS_CODES[exc.status_code] == "Forbidden"


def test_forbidden_custom_message_and_headers():
    """Providing a custom message and headers should set them correctly."""
    custom_msg = "Access denied"
    custom_headers = {"X-Custom-Header": "value"}
    exc = Forbidden(message=custom_msg, headers=custom_headers)
    assert exc.message == custom_msg
    assert exc.headers == custom_headers
    # The status code remains unchanged
    assert exc.status_code == 403
    # quiet should still be True by default
    assert exc.quiet is True


def test_forbidden_context_and_extra():
    """Context and extra data should be stored on the exception."""
    context = {"user_id": 42}
    extra = {"debug": True}
    exc = Forbidden(context=context, extra=extra)
    # The context should be accessible via the `context` attribute
    assert exc.context == context
    # The extra data should be stored in the `extra` attribute
    assert exc.extra == extra
    # The status code and quiet flag remain unchanged
    assert exc.status_code == 403
    assert exc.quiet is True
