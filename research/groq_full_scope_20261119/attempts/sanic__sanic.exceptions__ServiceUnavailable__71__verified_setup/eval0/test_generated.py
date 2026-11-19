import pytest
from sanic.exceptions import ServiceUnavailable


def test_service_unavailable_basic_attributes():
    """Verify that the ServiceUnavailable exception correctly stores
    the provided message, headers, and defaults for status_code and quiet."""
    msg = "Service temporarily down"
    hdrs = {"Retry-After": "120"}
    exc = ServiceUnavailable(msg, headers=hdrs)

    # status_code and quiet are class attributes
    assert exc.status_code == 503
    assert exc.quiet is True

    # message is stored on the instance
    assert exc.message == msg

    # headers are stored on the instance
    assert exc.headers == hdrs

    # context and extra default to None
    assert exc.context is None
    assert exc.extra is None


def test_service_unavailable_bytes_message_and_quiet_override():
    """Ensure that a bytes message is preserved and that the quiet flag
    can be overridden via the constructor."""
    msg_bytes = b"Binary error message"
    exc = ServiceUnavailable(msg_bytes, quiet=False)

    # message should be the original bytes object
    assert isinstance(exc.message, bytes)
    assert exc.message == msg_bytes

    # quiet flag should reflect the overridden value
    assert exc.quiet is False


def test_service_unavailable_invalid_headers_type():
    """Passing a non-dict type to headers should raise a TypeError."""
    with pytest.raises(TypeError):
        ServiceUnavailable("msg", headers=["not", "a", "dict"])
