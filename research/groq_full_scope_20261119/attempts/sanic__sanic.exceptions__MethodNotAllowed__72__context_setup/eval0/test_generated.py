import pytest
from sanic.exceptions import MethodNotAllowed


def test_default_initialization():
    """MethodNotAllowed without arguments should use default status and no Allow header."""
    exc = MethodNotAllowed()
    assert isinstance(exc, MethodNotAllowed)
    assert exc.status_code == 405
    assert exc.method == ""
    assert exc.allowed_methods is None
    # Default headers should not contain 'Allow'
    assert "Allow" not in exc.headers
    # Default message should be the status description
    assert exc.args[0] == "Method Not Allowed"


def test_allowed_methods_header_and_attributes():
    """Providing allowed_methods should set the Allow header and attributes correctly."""
    allowed = ["GET", "POST"]
    exc = MethodNotAllowed(method="PUT", allowed_methods=allowed)
    assert exc.method == "PUT"
    assert exc.allowed_methods == allowed
    # Allow header should be a comma‑separated string
    assert exc.headers.get("Allow") == "GET, POST"
    # The exception message remains the default status description
    assert exc.args[0] == "Method Not Allowed"


def test_message_bytes_and_custom_headers():
    """Message can be bytes and custom headers should merge correctly."""
    custom_headers = {"X-Custom": "value"}
    exc = MethodNotAllowed(message=b"Custom error", headers=custom_headers)
    # Bytes message should be decoded to str
    assert exc.args[0] == "Custom error"
    # Custom headers should be present
    assert exc.headers["X-Custom"] == "value"
    # No Allow header since none provided
    assert "Allow" not in exc.headers
