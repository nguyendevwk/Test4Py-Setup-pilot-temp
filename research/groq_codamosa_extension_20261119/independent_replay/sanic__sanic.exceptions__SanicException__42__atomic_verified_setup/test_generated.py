import pytest
from sanic.exceptions import SanicException
from sanic.helpers import STATUS_CODES


def test_default_initialization_and_status_code_from_status_codes():
    """SanicException should default to status_code 500 and use the
    corresponding status message when message is None."""
    exc = SanicException()
    assert exc.status_code == 500
    assert exc.message == STATUS_CODES[500].decode()
    assert exc.context is None
    assert exc.extra is None
    assert exc.headers == {}
    assert exc.quiet is False


def test_custom_message_and_headers_and_quiet_flag():
    """Providing a custom message, headers and quiet flag should override defaults."""
    custom_headers = {"X-Custom": "value"}
    exc = SanicException(
        "Custom error",
        status_code=418,
        quiet=True,
        headers=custom_headers,
        context={"detail": "extra info"},
        extra={"internal": "secret"},
    )
    assert exc.status_code == 418
    assert exc.message == "Custom error"
    assert exc.headers == custom_headers
    assert exc.quiet is True
    assert exc.context == {"detail": "extra info"}
    assert exc.extra == {"internal": "secret"}


def test_bytes_message_and_status_code_lookup():
    """When message is bytes, it should be decoded; if message is None,
    the status code lookup should provide the correct message."""
    # Bytes message
    exc_bytes = SanicException(b"Byte error", status_code=400)
    assert exc_bytes.message == "Byte error"
    assert exc_bytes.status_code == 400

    # None message with custom status code
    exc_none = SanicException(status_code=404)
    assert exc_none.message == STATUS_CODES[404].decode()
    assert exc_none.status_code == 404
