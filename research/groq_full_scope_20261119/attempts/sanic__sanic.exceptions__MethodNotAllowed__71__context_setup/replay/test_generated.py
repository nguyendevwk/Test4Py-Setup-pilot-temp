import pytest
from sanic.exceptions import MethodNotAllowed


def test_default_initialization():
    """MethodNotAllowed without arguments should use defaults."""
    exc = MethodNotAllowed()
    assert isinstance(exc, MethodNotAllowed)
    assert exc.status_code == 405
    assert exc.quiet is True
    # No custom message, so default status message should be used
    assert exc.message == "Method Not Allowed"
    # No Allow header when no allowed_methods provided
    assert "Allow" not in exc.headers
    # method and allowed_methods should be empty/None
    assert exc.method == ""
    assert exc.allowed_methods is None


def test_allowed_methods_header_and_attributes():
    """Providing allowed_methods should set the Allow header and attributes."""
    allowed = ["GET", "POST"]
    exc = MethodNotAllowed(allowed_methods=allowed, method="PUT")
    assert exc.allowed_methods == allowed
    assert exc.method == "PUT"
    # Allow header should contain comma‑separated methods
    assert exc.headers.get("Allow") == "GET, POST"
    # No other headers should be present
    assert set(exc.headers.keys()) == {"Allow"}


def test_message_bytes_and_custom_headers():
    """Message can be bytes and custom headers are merged correctly."""
    custom_headers = {"X-Custom": "value"}
    msg_bytes = b"Custom error message"
    exc = MethodNotAllowed(message=msg_bytes, headers=custom_headers)
    # Bytes message should be decoded to str
    assert exc.message == "Custom error message"
    # Custom headers should be present
    assert exc.headers["X-Custom"] == "value"
    # No Allow header since allowed_methods not provided
    assert "Allow" not in exc.headers
