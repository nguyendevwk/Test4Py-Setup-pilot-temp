import pytest
from sanic.exceptions import InvalidHeader
from sanic.helpers import STATUS_CODES

def test_invalid_header_default_message_and_status():
    """InvalidHeader without message should use default status code and default message."""
    exc = InvalidHeader()
    # Status code should be 400
    assert exc.status == 400
    # Default message should be the status description
    assert exc.message == STATUS_CODES[400]
    # No headers should be present
    assert exc.headers == {}

def test_invalid_header_custom_message_and_headers():
    """Providing a custom message and headers should reflect in the exception."""
    custom_msg = "Invalid header value"
    custom_headers = {"X-Custom-Error": "True"}
    exc = InvalidHeader(message=custom_msg, headers=custom_headers)
    assert exc.message == custom_msg
    assert exc.headers == custom_headers
    # Status remains 400
    assert exc.status == 400

def test_invalid_header_context_and_extra():
    """Context and extra data should be stored correctly and not affect status."""
    context = {"field": "value"}
    extra = {"debug": "info"}
    exc = InvalidHeader(context=context, extra=extra)
    assert exc.context == context
    assert exc.extra == extra
    # Status remains 400
    assert exc.status == 400
