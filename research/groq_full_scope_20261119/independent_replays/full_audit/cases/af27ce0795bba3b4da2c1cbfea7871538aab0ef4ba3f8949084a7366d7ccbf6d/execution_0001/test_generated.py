import pytest
from sanic.exceptions import MethodNotAllowed


def test_default_initialization():
    """MethodNotAllowed should default to status 405, quiet True, and no Allow header."""
    exc = MethodNotAllowed()
    assert exc.status_code == 405
    assert exc.quiet is True
    # The base HTTPException sets a default message if None is passed
    assert isinstance(exc.message, str) or isinstance(exc.message, bytes)
    # No Allow header should be present
    assert "Allow" not in exc.headers
    # method and allowed_methods should be the defaults
    assert exc.method == ""
    assert exc.allowed_methods is None


def test_allowed_methods_header():
    """Providing allowed_methods should set the Allow header correctly."""
    allowed = ["GET", "POST", "PUT"]
    exc = MethodNotAllowed(allowed_methods=allowed)
    # Allow header should be a comma‑separated string of the methods
    assert exc.headers.get("Allow") == ", ".join(allowed)
    # The allowed_methods attribute should be the original sequence
    assert exc.allowed_methods == allowed
    # method remains the default
    assert exc.method == ""


def test_custom_message_and_method():
    """Custom message and method should be stored on the exception."""
    msg = "Custom error message"
    method = "DELETE"
    exc = MethodNotAllowed(message=msg, method=method)
    assert exc.message == msg
    assert exc.method == method
    # No Allow header should be present when allowed_methods is None
    assert "Allow" not in exc.headers
