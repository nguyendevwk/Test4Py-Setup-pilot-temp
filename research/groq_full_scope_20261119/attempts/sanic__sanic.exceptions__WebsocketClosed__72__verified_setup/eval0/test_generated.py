import pytest
from sanic.exceptions import WebsocketClosed


def test_default_initialization(tmp_path):
    """WebsocketClosed should initialize with default attributes."""
    exc = WebsocketClosed()
    # Default message should be the class message
    assert exc.message == "Client has closed the websocket connection"
    # quiet flag defaults to True
    assert exc.quiet is True
    # status_code should be None by default
    assert exc.status_code is None
    # context and extra should be empty dicts
    assert exc.context == {}
    assert exc.extra == {}


def test_custom_parameters():
    """Custom parameters should override defaults."""
    exc = WebsocketClosed(
        message="Custom error",
        status_code=499,
        quiet=False,
        context={"key": "value"},
        extra={"extra_key": 123},
        headers={"X-Custom": "header"},
    )
    assert exc.message == "Custom error"
    assert exc.status_code == 499
    assert exc.quiet is False
    assert exc.context == {"key": "value"}
    assert exc.extra == {"extra_key": 123}
    assert exc.headers == {"X-Custom": "header"}


def test_invalid_status_code_type():
    """Providing a non‑int status_code should raise a TypeError."""
    with pytest.raises(TypeError):
        WebsocketClosed(status_code="not-an-int")
