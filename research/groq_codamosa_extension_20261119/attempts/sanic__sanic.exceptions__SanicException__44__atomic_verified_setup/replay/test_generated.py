import pytest
from sanic.exceptions import SanicException
from sanic.helpers import STATUS_CODES


def test_default_initialization():
    """SanicException with no arguments should use defaults."""
    exc = SanicException()
    # Default status code is class attribute 500
    assert exc.status_code == 500
    # Default quiet is False
    assert exc.quiet is False
    # Default headers is empty dict
    assert exc.headers == {}
    # Message should be the standard reason phrase for 500
    assert exc.args[0] == STATUS_CODES[500].decode()
    # context and extra should be None
    assert exc.context is None
    assert exc.extra is None


def test_custom_status_and_message_bytes():
    """Providing a bytes message and custom status should decode correctly."""
    raw_msg = b"Custom error"
    exc = SanicException(raw_msg, status_code=418)
    # Status code set to 418
    assert exc.status_code == 418
    # Message decoded from bytes
    assert exc.args[0] == "Custom error"
    # Quiet should remain default False
    assert exc.quiet is False
    # Headers should remain default empty dict
    assert exc.headers == {}


def test_context_extra_and_headers():
    """Context, extra, and headers are stored correctly."""
    ctx = {"detail": "Something went wrong"}
    extra = {"internal": "debug info"}
    hdrs = {"X-Custom": "value"}
    exc = SanicException(
        "Error occurred",
        status_code=400,
        context=ctx,
        extra=extra,
        headers=hdrs,
    )
    # Status code and message
    assert exc.status_code == 400
    assert exc.args[0] == "Error occurred"
    # Context and extra preserved
    assert exc.context == ctx
    assert exc.extra == extra
    # Headers preserved
    assert exc.headers == hdrs
    # Quiet remains default
    assert exc.quiet is False
