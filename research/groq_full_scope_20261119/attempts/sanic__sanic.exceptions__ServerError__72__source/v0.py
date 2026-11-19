import pytest
from sanic.exceptions import ServerError
from sanic.helpers import STATUS_CODES


def test_default_server_error_initialization():
    """ServerError without arguments should default to status 500 and no message."""
    err = ServerError()
    assert err.status_code == 500
    assert err.message is None
    assert err.headers == {}
    # The default description should match the status code description
    assert err.description == STATUS_CODES[500]


def test_server_error_with_custom_message_and_headers():
    """ServerError should store custom message and headers correctly."""
    custom_msg = "Something went wrong"
    custom_headers = {"X-Custom": "value", "Content-Type": "text/plain"}
    err = ServerError(message=custom_msg, headers=custom_headers)
    assert err.status_code == 500
    assert err.message == custom_msg
    assert err.headers == custom_headers
    # The description should still be the default status description
    assert err.description == STATUS_CODES[500]


def test_server_error_quiet_and_context_behavior():
    """ServerError should preserve quiet flag and context mapping."""
    context = {"user_id": 42, "action": "test"}
    err = ServerError(message="Error", quiet=True, context=context)
    assert err.quiet is True
    assert err.context == context
    # Ensure that the context is not part of the headers
    assert "user_id" not in err.headers
    # The description remains the default
    assert err.description == STATUS_CODES[500]
