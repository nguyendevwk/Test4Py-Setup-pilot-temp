import pytest
from sanic.exceptions import WebsocketClosed


def test_default_initialization():
    """WebsocketClosed should use the class defaults when no arguments are supplied."""
    exc = WebsocketClosed()
    # The default message is defined on the class
    assert exc.args[0] == "Client has closed the websocket connection"
    # Default status_code comes from SanicException (500) unless overridden
    assert exc.status_code == 500
    # quiet flag should be True as defined on the subclass
    assert exc.quiet is True
    # No headers should be present by default
    assert exc.headers == {}


def test_bytes_message_and_custom_status():
    """Providing a bytes message and a custom status code should set the attributes correctly."""
    raw_msg = b"Connection lost"
    exc = WebsocketClosed(raw_msg, status_code=400)
    # Bytes message should be decoded to str
    assert exc.args[0] == "Connection lost"
    # Custom status code should override the default
    assert exc.status_code == 400
    # quiet flag remains True from the subclass
    assert exc.quiet is True
    # Headers should still be empty
    assert exc.headers == {}


def test_context_and_headers_propagation():
    """Context and headers passed to the constructor should be stored on the exception."""
    ctx = {"user": "alice", "action": "disconnect"}
    hdrs = {"X-Reason": "timeout"}
    exc = WebsocketClosed(
        "User disconnected",
        status_code=410,
        context=ctx,
        headers=hdrs,
    )
    # The message should be set correctly
    assert exc.args[0] == "User disconnected"
    # Status code should be the one provided
    assert exc.status_code == 410
    # Context should be stored on the instance
    assert exc.context == ctx
    # Headers should be stored on the instance
    assert exc.headers == hdrs
    # quiet flag remains True from the subclass
    assert exc.quiet is True
