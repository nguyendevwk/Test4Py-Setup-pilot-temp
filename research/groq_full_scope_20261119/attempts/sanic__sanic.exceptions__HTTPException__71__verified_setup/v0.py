import pytest
from sanic.exceptions import HTTPException


def test_http_exception_basic_message_and_attributes():
    """Verify that a basic HTTPException stores the message and default attributes."""
    exc = HTTPException("Not Found")
    assert isinstance(exc, HTTPException)
    # The message should be stored as a string
    assert exc.args[0] == "Not Found"
    # Default quiet flag is None
    assert exc.quiet is None
    # Context, extra, headers default to empty dicts
    assert exc.context == {}
    assert exc.extra == {}
    assert exc.headers == {}


def test_http_exception_with_headers_and_quiet_flag():
    """Verify that headers and quiet flag are correctly set and accessible."""
    headers = {"Content-Type": "application/json", "X-Test": "value"}
    exc = HTTPException("Error", quiet=True, headers=headers)
    # quiet flag should be True
    assert exc.quiet is True
    # Headers should be stored exactly as passed
    assert exc.headers == headers
    # The message should be stored as a string
    assert exc.args[0] == "Error"


def test_http_exception_with_bytes_message_and_context():
    """Verify that a bytes message is accepted and context is stored."""
    context = {"user_id": 42}
    exc = HTTPException(b"Binary error", context=context)
    # Bytes message should be stored as bytes
    assert isinstance(exc.args[0], bytes)
    assert exc.args[0] == b"Binary error"
    # Context should be stored correctly
    assert exc.context == context
    # Extra and headers should be empty dicts
    assert exc.extra == {}
    assert exc.headers == {}
