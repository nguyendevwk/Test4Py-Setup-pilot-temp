import pytest
from sanic.exceptions import ServerError
from sanic.helpers import STATUS_CODES

def test_server_error_basic_attributes():
    """ServerError should expose the correct status code and default message."""
    err = ServerError()
    # Status code must be 500
    assert err.status_code == 500
    # Default message is None
    assert err.message is None
    # The default description should be the status phrase
    assert err.description == STATUS_CODES[500]
    # No headers, context or extra by default
    assert err.headers == {}
    assert err.context == {}
    assert err.extra == {}

def test_server_error_with_bytes_message_and_headers():
    """ServerError should accept a bytes message and custom headers."""
    msg = b"binary error"
    hdrs = {"X-Custom": "value"}
    err = ServerError(message=msg, headers=hdrs)
    # Message should be stored as bytes
    assert err.message == msg
    # Headers should be reflected
    assert err.headers == hdrs
    # Status code remains 500
    assert err.status_code == 500

def test_server_error_invalid_headers_type_raises():
    """Passing a non-dict to headers should raise a TypeError."""
    with pytest.raises(TypeError):
        ServerError(headers="not a dict")
