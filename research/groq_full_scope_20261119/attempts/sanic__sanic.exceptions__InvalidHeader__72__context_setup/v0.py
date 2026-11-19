import pytest
from sanic.exceptions import InvalidHeader
from sanic.exceptions import BadRequest

def test_invalid_header_basic_properties():
    """InvalidHeader should inherit BadRequest and expose expected attributes."""
    exc = InvalidHeader("Bad header")
    # Inherits status_code from BadRequest
    assert exc.status_code == 400
    # quiet defaults to True from BadRequest
    assert exc.quiet is True
    # message is stored
    assert exc.message == "Bad header"
    # context, extra, headers default to None
    assert exc.context is None
    assert exc.extra is None
    assert exc.headers is None

def test_invalid_header_with_headers():
    """Providing custom headers should be reflected in the exception."""
    custom_headers = {"X-Custom": "value", "Content-Type": "text/plain"}
    exc = InvalidHeader("Header error", headers=custom_headers)
    # Headers should be stored exactly as provided
    assert exc.headers == custom_headers
    # The exception should still have status_code 400
    assert exc.status_code == 400

def test_invalid_header_message_type_bytes():
    """Message can be bytes and should be preserved."""
    msg_bytes = b"binary header"
    exc = InvalidHeader(msg_bytes)
    # The message attribute should be the same bytes object
    assert isinstance(exc.message, bytes)
    assert exc.message == msg_bytes
