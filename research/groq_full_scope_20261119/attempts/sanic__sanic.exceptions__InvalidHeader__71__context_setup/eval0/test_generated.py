import pytest
from sanic.exceptions import InvalidHeader

def test_invalid_header_basic_message_and_status():
    """Creating an InvalidHeader with a message sets the message and status code."""
    exc = InvalidHeader("Invalid header value")
    assert isinstance(exc, InvalidHeader)
    assert exc.status_code == 400
    assert exc.message == "Invalid header value"
    # The default quiet flag from BadRequest should be True
    assert exc.quiet is True

def test_invalid_header_with_custom_headers_and_context():
    """Custom headers and context are preserved on the exception."""
    custom_headers = {"X-Custom-Error": "true"}
    context = {"field": "value"}
    exc = InvalidHeader("Bad header", headers=custom_headers, context=context)
    # Headers should be stored in the exception's headers attribute
    assert exc.headers == custom_headers
    # Context should be stored in the exception's context attribute
    assert exc.context == context

def test_invalid_header_default_quiet_and_extra():
    """When quiet and extra are not provided, they default to the values defined in BadRequest."""
    exc = InvalidHeader()
    # quiet should default to True as defined in BadRequest
    assert exc.quiet is True
    # extra should default to None
    assert exc.extra is None
