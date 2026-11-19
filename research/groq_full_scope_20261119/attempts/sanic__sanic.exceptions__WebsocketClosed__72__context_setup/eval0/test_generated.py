import pytest
from sanic.exceptions import WebsocketClosed
from sanic.helpers import STATUS_CODES

def test_default_initialization():
    """WebsocketClosed should use class defaults when no arguments are provided."""
    exc = WebsocketClosed()
    # Default message defined on the class
    assert exc.args[0] == WebsocketClosed.message
    # Default status code from SanicException
    assert exc.status_code == 500
    # quiet flag should be True as defined on the subclass
    assert exc.quiet is True
    # No headers by default
    assert exc.headers == {}
    # Context and extra should be None
    assert exc.context is None
    assert exc.extra is None

def test_custom_message_and_status():
    """Providing a custom message and status code should override defaults."""
    custom_msg = "Custom websocket close reason"
    custom_status = 400
    exc = WebsocketClosed(custom_msg, custom_status)
    assert exc.args[0] == custom_msg
    assert exc.status_code == custom_status
    # quiet should still be True from the subclass
    assert exc.quiet is True
    # Headers remain default
    assert exc.headers == {}
    # Context and extra remain None
    assert exc.context is None
    assert exc.extra is None

def test_bytes_message_and_headers():
    """Bytes message should be decoded and custom headers should be preserved."""
    bytes_msg = b"Binary close reason"
    headers = {"X-Custom": "value"}
    exc = WebsocketClosed(bytes_msg, headers=headers)
    # Bytes should be decoded to string
    assert exc.args[0] == "Binary close reason"
    # Status code should default to 500
    assert exc.status_code == 500
    # Headers should match the provided dict
    assert exc.headers == headers
    # quiet remains True
    assert exc.quiet is True
