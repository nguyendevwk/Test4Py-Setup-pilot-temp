import pytest
from sanic.exceptions import WebsocketClosed
from sanic.exceptions import SanicException


def test_default_initialization():
    """WebsocketClosed should initialize with default message and quiet flag."""
    exc = WebsocketClosed()
    # Default message should match the class attribute
    assert exc.message == "Client has closed the websocket connection"
    # quiet flag should be True by default
    assert exc.quiet is True
    # status_code should be None unless explicitly set
    assert exc.status_code is None
    # The exception should be an instance of SanicException
    assert isinstance(exc, SanicException)


def test_custom_message_and_status():
    """Providing a custom message and status_code should override defaults."""
    custom_msg = "Custom close reason"
    custom_status = 499
    exc = WebsocketClosed(message=custom_msg, status_code=custom_status)
    assert exc.message == custom_msg
    assert exc.status_code == custom_status
    # quiet flag remains True unless overridden
    assert exc.quiet is True
    # The exception should still be a SanicException
    assert isinstance(exc, SanicException)


def test_quiet_flag_override_and_context():
    """The quiet flag can be overridden and context can be set."""
    exc = WebsocketClosed(quiet=False, context={"user": "alice"})
    # quiet flag should reflect the overridden value
    assert exc.quiet is False
    # context should be stored correctly
    assert exc.context == {"user": "alice"}
    # message remains default
    assert exc.message == "Client has closed the websocket connection"
    # status_code remains None
    assert exc.status_code is None
