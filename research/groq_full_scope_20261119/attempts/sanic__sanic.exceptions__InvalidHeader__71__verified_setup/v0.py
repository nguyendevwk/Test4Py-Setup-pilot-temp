import pytest
from sanic.exceptions import InvalidHeader


def test_invalid_header_initialization_with_message_and_headers():
    """Verify that the exception stores the provided message and headers."""
    msg = "Invalid header value"
    hdrs = {"X-Custom": "value"}
    exc = InvalidHeader(msg, headers=hdrs)

    # The message should be stored in the exception's args
    assert exc.args[0] == msg

    # The headers should be accessible via the `headers` attribute
    assert hasattr(exc, "headers")
    assert exc.headers == hdrs

    # The exception should be an instance of BadRequest (via inheritance)
    from sanic.exceptions import BadRequest
    assert isinstance(exc, BadRequest)


def test_invalid_header_default_behavior():
    """Verify that default construction yields a 400 status and no message."""
    exc = InvalidHeader()

    # Default message should be None, resulting in a generic "Bad Request" message
    assert exc.args[0] is None

    # No headers should be set by default
    assert getattr(exc, "headers", None) is None

    # The exception should have the correct HTTP status code (400)
    assert exc.status == 400


def test_invalid_header_invalid_headers_type():
    """Passing a non-dict to headers should raise a TypeError."""
    with pytest.raises(TypeError):
        InvalidHeader("msg", headers="not-a-dict")
