import pytest
from sanic.exceptions import Forbidden
from sanic.helpers import STATUS_CODES


def test_default_forbidden_attributes():
    """Forbidden should default to status 403 and quiet True."""
    exc = Forbidden()
    assert exc.status_code == 403
    assert exc.quiet is True
    # The default message is None, but the exception should still carry the status code
    assert exc.message is None
    # The status description should match the status code
    assert STATUS_CODES[exc.status_code] == "Forbidden"


def test_forbidden_with_custom_message_and_headers():
    """Providing a custom message and headers should set them correctly."""
    custom_msg = "Access denied"
    custom_headers = {"X-Custom-Header": "value"}
    exc = Forbidden(message=custom_msg, headers=custom_headers)
    assert exc.message == custom_msg
    assert exc.headers == custom_headers
    # The status code remains unchanged
    assert exc.status_code == 403
    # The quiet flag should still be True by default
    assert exc.quiet is True


def test_forbidden_context_and_extra_data():
    """Context and extra data should be stored on the exception."""
    context = {"user_id": 42}
    extra = {"debug": True}
    exc = Forbidden(context=context, extra=extra)
    # Context should be accessible via the `context` attribute
    assert exc.context == context
    # Extra data should be stored in the `extra` attribute
    assert exc.extra == extra
    # The status code and quiet flag remain unchanged
    assert exc.status_code == 403
    assert exc.quiet is True
