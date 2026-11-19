import pytest
from sanic.exceptions import BadRequest


def test_default_initialization():
    """BadRequest should initialize with default values."""
    exc = BadRequest()
    assert exc.status_code == 400
    # Default message is None, which should result in the default status phrase
    assert exc.message is None
    # quiet defaults to True as defined in the class
    assert exc.quiet is True
    # No context, extra, or headers by default
    assert exc.context is None
    assert exc.extra is None
    assert exc.headers is None


def test_custom_message_and_headers():
    """Providing a custom message and headers should store them correctly."""
    custom_msg = "Invalid input data"
    custom_headers = {"X-Custom-Header": "value"}
    exc = BadRequest(custom_msg, headers=custom_headers)
    assert exc.message == custom_msg
    assert exc.headers == custom_headers
    # quiet should remain True unless explicitly overridden
    assert exc.quiet is True
    # context and extra remain None
    assert exc.context is None
    assert exc.extra is None


def test_invalid_message_type_raises():
    """BadRequest should raise a TypeError when message is not str, bytes, or None."""
    with pytest.raises(TypeError):
        BadRequest(123)  # int is not an allowed type for message
