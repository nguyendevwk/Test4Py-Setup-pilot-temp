import pytest
from sanic.exceptions import PayloadTooLarge
from sanic.helpers import STATUS_CODES


def test_payload_too_large_default_initialization():
    """Default construction should set status_code, quiet, and empty headers."""
    exc = PayloadTooLarge()
    assert exc.status_code == 413
    assert exc.quiet is True
    assert exc.headers == {}
    # Default message should be the status code description
    assert exc.args[0] == STATUS_CODES[413].decode()


def test_payload_too_large_with_bytes_and_custom_headers():
    """Providing a bytes message and custom headers should override defaults."""
    custom_headers = {"X-Custom": "value"}
    exc = PayloadTooLarge(b"Too big!", headers=custom_headers)
    assert exc.status_code == 413
    assert exc.quiet is True
    assert exc.headers == custom_headers
    # Bytes message should be decoded to str
    assert exc.args[0] == "Too big!"


def test_payload_too_large_invalid_message_type_raises():
    """Passing an unsupported message type should raise a TypeError."""
    with pytest.raises(TypeError):
        PayloadTooLarge(123)  # int is not allowed
