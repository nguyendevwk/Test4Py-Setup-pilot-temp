import pytest
from sanic.exceptions import MethodNotAllowed


def test_default_initialization():
    """MethodNotAllowed should default to status 405, quiet True, and no Allow header."""
    exc = MethodNotAllowed()
    assert exc.status_code == 405
    assert exc.quiet is True
    assert exc.method == ""
    assert exc.allowed_methods is None
    # No Allow header when no allowed_methods provided
    assert "Allow" not in exc.headers


def test_allowed_methods_header_and_attributes():
    """Providing allowed_methods should set the Allow header and attributes correctly."""
    allowed = ["GET", "POST"]
    exc = MethodNotAllowed(method="PUT", allowed_methods=allowed)
    assert exc.method == "PUT"
    assert exc.allowed_methods == allowed
    # Allow header should be a comma‑separated string of the methods
    assert exc.headers["Allow"] == "GET, POST"
    # The header should not overwrite any other headers
    assert exc.headers.get("Content-Type") is None


def test_message_and_quiet_override():
    """Message and quiet parameters should override defaults."""
    exc = MethodNotAllowed(message="Custom error", quiet=False)
    # The message should be stored in the exception (HTTPException stores it in .message)
    assert exc.message == "Custom error"
    # quiet should be overridden to False
    assert exc.quiet is False
