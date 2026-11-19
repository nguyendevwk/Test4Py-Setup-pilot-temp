import pytest
from sanic.exceptions import WebsocketClosed

def test_websocket_closed_attributes():
    """Verify the class attributes and default message."""
    exc = WebsocketClosed()
    # The exception should be quiet and have the expected message
    assert exc.quiet is True
    assert exc.message == "Client has closed the websocket connection"
    # The string representation should include the message
    assert str(exc) == exc.message

def test_websocket_closed_inherits_exception():
    """Ensure WebsocketClosed behaves like a normal exception."""
    exc = WebsocketClosed()
    # It should be an instance of Exception and SanicException
    assert isinstance(exc, Exception)
    # Raising and catching should preserve the original instance
    try:
        raise exc
    except WebsocketClosed as caught:
        assert caught is exc
    else:
        pytest.fail("WebsocketClosed was not caught")

def test_websocket_closed_with_custom_message():
    """Test that a custom message can override the default."""
    custom_msg = "Custom websocket closed message"
    exc = WebsocketClosed(message=custom_msg)
    # The custom message should be used
    assert exc.message == custom_msg
    assert str(exc) == custom_msg
