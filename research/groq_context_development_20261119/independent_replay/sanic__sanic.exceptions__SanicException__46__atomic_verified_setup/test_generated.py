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
        extra={"internal": "data"},
    )
    assert isinstance(exc, SanicException)
    assert exc.args[0] == "Custom error"
    assert exc.status_code == 418
    assert exc.headers == {"X-Custom": "value"}
    assert exc.quiet is True
    assert exc.context == {"detail": "extra"}
    assert exc.extra == {"internal": "data"}
    # The message attribute should match the provided message
    assert exc.message == "Custom error"


def test_sanic_exception_default_message_from_status_code():
    # When message is None, the exception should use the status code's standard phrase
    exc = SanicException(status_code=404)
    expected_message = STATUS_CODES[404].decode()
    assert exc.args[0] == expected_message
    assert exc.status_code == 404
    assert exc.message == expected_message
    # No headers or context should be set by default
    assert exc.headers == {}
    assert exc.context is None
    assert exc.extra is None


def test_sanic_exception_bytes_message_decoded_and_default_status():
    # Passing a bytes message should be decoded to str
    exc = SanicException(b"Byte message")
    assert exc.args[0] == "Byte message"
    assert exc.message == "Byte message"
    # Default status code should be the class default (500)
    assert exc.status_code == 500
    # Quiet should be the class default (False)
    assert exc.quiet is False
