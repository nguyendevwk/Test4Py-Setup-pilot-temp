import pytest
from sanic.exceptions import URITooLong
from sanic.helpers import STATUS_CODES


def test_default_message_and_status():
    """URITooLong without arguments should use default status and message."""
    exc = URITooLong()
    # status_code should be 414 as defined in the class
    assert exc.status_code == 414
    # message should be the standard reason phrase for 414
    assert exc.message == STATUS_CODES[414].decode()
    # quiet flag should be True as defined in the class
    assert exc.quiet is True
    # headers should be empty dict by default
    assert exc.headers == {}


def test_custom_message_and_headers():
    """Providing a custom message and headers should override defaults."""
    custom_msg = "Custom URI too long error"
    custom_headers = {"X-Custom": "value"}
    exc = URITooLong(custom_msg, headers=custom_headers)
    # status_code remains 414
    assert exc.status_code == 414
    # message should be the custom string
    assert exc.message == custom_msg
    # quiet flag remains True
    assert exc.quiet is True
    # headers should match the custom dict
    assert exc.headers == custom_headers


def test_context_and_extra_are_stored():
    """Context and extra parameters should be stored on the exception."""
    ctx = {"path": "/very/long/url"}
    extra = {"debug": True}
    exc = URITooLong(context=ctx, extra=extra)
    # context and extra should be accessible as attributes
    assert exc.context == ctx
    assert exc.extra == extra
    # status_code and message should still be defaults
    assert exc.status_code == 414
    assert exc.message == STATUS_CODES[414].decode()
