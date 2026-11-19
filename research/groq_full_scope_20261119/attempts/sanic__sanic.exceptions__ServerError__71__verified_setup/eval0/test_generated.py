import pytest
from sanic.exceptions import ServerError


def test_server_error_basic():
    """ServerError should store provided message, quiet flag, context, extra and headers."""
    msg = "Something went wrong"
    context = {"user_id": 42}
    extra = {"debug": "stacktrace"}
    headers = {"X-Custom": "value"}

    exc = ServerError(
        msg,
        quiet=True,
        context=context,
        extra=extra,
        headers=headers,
    )

    assert exc.status_code == 500
    assert exc.message == msg
    assert exc.quiet is True
    assert exc.context == context
    assert exc.extra == extra
    assert exc.headers == headers


def test_server_error_none_message_and_default_headers():
    """When message is None, ServerError should default to a generic message and
    allow empty headers."""
    exc = ServerError(None, quiet=False, context=None, extra=None, headers={})
    assert exc.status_code == 500
    # The default message is the status description
    assert exc.message == "Internal Server Error"
    assert exc.quiet is False
    assert exc.context is None
    assert exc.extra is None
    assert exc.headers == {}


def test_server_error_invalid_message_type():
    """Passing a non-string/non-bytes message should raise a TypeError."""
    with pytest.raises(TypeError):
        ServerError(123)  # type: ignore[arg-type]
