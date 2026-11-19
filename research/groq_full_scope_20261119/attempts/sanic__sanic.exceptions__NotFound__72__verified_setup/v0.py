import pytest
from sanic.exceptions import NotFound
from sanic.helpers import STATUS_CODES


def test_notfound_default_attributes():
    """Verify default status code, quiet flag, and default message handling."""
    exc = NotFound()
    # status_code should be 404
    assert exc.status_code == 404
    # quiet should default to True
    assert exc.quiet is True
    # message should be None, so default status message is used
    assert exc.message is None
    # The default status message should match the STATUS_CODES mapping
    assert STATUS_CODES[404] == "Not Found"


def test_notfound_custom_message_and_headers():
    """Verify that custom message and headers are stored correctly."""
    custom_msg = "Custom not found error"
    custom_headers = {"X-Custom-Header": "value"}
    exc = NotFound(custom_msg, headers=custom_headers)
    # message should be set to the custom string
    assert exc.message == custom_msg
    # headers should be stored in the exception
    assert exc.headers == custom_headers
    # quiet should remain True unless explicitly overridden
    assert exc.quiet is True


def test_notfound_context_and_extra():
    """Verify that context and extra data are stored and accessible."""
    context_data = {"resource": "/missing"}
    extra_data = {"debug": "info"}
    exc = NotFound(context=context_data, extra=extra_data)
    # context should be stored
    assert exc.context == context_data
    # extra should be stored
    assert exc.extra == extra_data
    # message remains None
    assert exc.message is None
