import pytest
from sanic.exceptions import ServerError


def test_server_error_basic_initialization():
    """ServerError should store the provided message and default attributes."""
    err = ServerError("Something went wrong")
    assert err.status_code == 500
    assert err.message == "Something went wrong"
    # Default quiet, context, extra, headers should be None
    assert err.quiet is None
    assert err.context is None
    assert err.extra is None
    assert err.headers is None


def test_server_error_with_all_parameters(tmp_path):
    """ServerError should correctly handle all optional parameters."""
    custom_headers = {"X-Custom": "value"}
    context = {"user_id": 123}
    extra = {"debug": True}
    err = ServerError(
        b"binary message",
        quiet=True,
        context=context,
        extra=extra,
        headers=custom_headers,
    )
    assert err.status_code == 500
    assert err.message == b"binary message"
    assert err.quiet is True
    assert err.context == context
    assert err.extra == extra
    assert err.headers == custom_headers
    # Ensure that the headers are accessible via the response object if needed
    # (Sanic's HTTPException typically exposes headers directly)
    assert err.headers["X-Custom"] == "value"


def test_server_error_invalid_message_type():
    """Providing a non-string/bytes message should raise a TypeError."""
    with pytest.raises(TypeError):
        ServerError(42)  # int is not an acceptable message type
