import pytest
from sanic.exceptions import HTTPException


def test_http_exception_basic_initialization():
    """Verify that HTTPException stores the message and default attributes."""
    exc = HTTPException("Not Found")
    assert isinstance(exc, HTTPException)
    assert exc.args[0] == "Not Found"
    # Default quiet should be False (inherited from SanicException)
    assert exc.quiet is False
    # Context, extra, headers should be empty dicts if not provided
    assert exc.context == {}
    assert exc.extra == {}
    assert exc.headers == {}


def test_http_exception_with_bytes_and_headers():
    """Check that bytes message and custom headers are handled correctly."""
    headers = {"Content-Type": "text/plain", "X-Custom": "value"}
    exc = HTTPException(b"Binary message", headers=headers)
    assert isinstance(exc, HTTPException)
    assert exc.args[0] == b"Binary message"
    assert exc.headers == headers
    # Ensure that quiet can be set to True
    exc2 = HTTPException("Quiet", quiet=True)
    assert exc2.quiet is True


def test_http_exception_invalid_message_type():
    """Passing an invalid message type should raise a TypeError."""
    with pytest.raises(TypeError):
        # The constructor expects str, bytes, or None; int is invalid
        HTTPException(123)
