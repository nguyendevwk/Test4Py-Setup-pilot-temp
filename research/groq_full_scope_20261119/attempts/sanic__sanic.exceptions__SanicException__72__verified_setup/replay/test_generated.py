import pytest
from sanic.exceptions import SanicException
from sanic.helpers import STATUS_CODES


def test_sanic_exception_with_all_parameters():
    """SanicException should store all provided attributes correctly."""
    exc = SanicException(
        message="Error occurred",
        status_code=418,
        quiet=True,
        context={"detail": "test"},
        extra={"internal": "secret"},
        headers={"X-Custom": "value"},
    )
    assert isinstance(exc, SanicException)
    assert exc.args[0] == "Error occurred"
    assert exc.status_code == 418
    assert exc.quiet is True
    assert exc.context == {"detail": "test"}
    assert exc.extra == {"internal": "secret"}
    assert exc.headers == {"X-Custom": "value"}


def test_sanic_exception_default_message_from_status_code():
    """When message is None, the exception should use the status code's default message."""
    # 404 is a common status code with a known message
    exc = SanicException(status_code=404)
    expected_message = STATUS_CODES[404].decode()
    assert exc.args[0] == expected_message
    assert exc.status_code == 404
    assert exc.message == expected_message


def test_sanic_exception_bytes_message_decoded():
    """Bytes messages should be decoded to str."""
    byte_msg = b"Binary error"
    exc = SanicException(message=byte_msg, status_code=400)
    assert exc.args[0] == "Binary error"
    assert exc.status_code == 400
    assert isinstance(exc.args[0], str)
