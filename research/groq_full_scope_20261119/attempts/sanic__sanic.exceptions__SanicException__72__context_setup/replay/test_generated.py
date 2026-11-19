import pytest
from sanic.exceptions import SanicException
from sanic.helpers import STATUS_CODES

def test_sanic_exception_with_custom_message_and_headers():
    exc = SanicException(
        "Custom error",
        status_code=418,
        headers={"X-Custom": "value"},
        quiet=True,
        context={"detail": "extra"},
        extra={"internal": "info"},
    )
    assert isinstance(exc, SanicException)
    assert exc.args[0] == "Custom error"
    assert exc.status_code == 418
    assert exc.headers == {"X-Custom": "value"}
    assert exc.quiet is True
    assert exc.context == {"detail": "extra"}
    assert exc.extra == {"internal": "info"}

def test_sanic_exception_default_message_from_status_code():
    # STATUS_CODES contains mapping for 404
    exc = SanicException(status_code=404)
    expected_message = STATUS_CODES[404].decode()
    assert exc.args[0] == expected_message
    assert exc.status_code == 404
    assert exc.message == expected_message

def test_sanic_exception_bytes_message_decoded():
    exc = SanicException(b"Byte message", status_code=400)
    assert exc.args[0] == "Byte message"
    assert exc.status_code == 400
    assert exc.message == "Byte message"
