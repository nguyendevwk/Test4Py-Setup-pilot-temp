import pytest
from sanic.exceptions import MethodNotAllowed


def test_default_initialization():
    """MethodNotAllowed without arguments should use default status and quiet flag."""
    exc = MethodNotAllowed()
    # Status code is set by the class
    assert exc.status_code == 405
    # quiet defaults to True as defined in the class
    assert exc.quiet is True
    # No method or allowed_methods set
    assert exc.method == ""
    assert exc.allowed_methods is None
    # No custom headers added
    assert "Allow" not in exc.headers


def test_allowed_methods_header_and_method():
    """Providing allowed_methods should set the Allow header and store method."""
    allowed = ["GET", "POST"]
    exc = MethodNotAllowed(method="PUT", allowed_methods=allowed)
    # The Allow header should contain the methods joined by comma and space
    assert exc.headers.get("Allow") == "GET, POST"
    # The method attribute should reflect the provided method
    assert exc.method == "PUT"
    # allowed_methods attribute should be the same sequence
    assert exc.allowed_methods == allowed


def test_message_and_bytes_handling():
    """Message can be a string or bytes; it should be stored unchanged."""
    msg_str = "Custom error message"
    exc_str = MethodNotAllowed(message=msg_str)
    assert exc_str.message == msg_str

    msg_bytes = b"Binary error message"
    exc_bytes = MethodNotAllowed(message=msg_bytes)
    assert exc_bytes.message == msg_bytes
