import pytest
from sanic.exceptions import SanicException
from sanic.helpers import STATUS_CODES

def test_sanic_exception_basic_initialization():
    exc = SanicException("Error occurred", status_code=404, quiet=True, headers={"X-Test": "value"})
    assert isinstance(exc, SanicException)
    assert exc.args[0] == "Error occurred"
    assert exc.status_code == 404
    assert exc.quiet is True
    assert exc.headers == {"X-Test": "value"}
    assert exc.context is None
    assert exc.extra is None

def test_sanic_exception_default_message_from_status_code():
    # When message is None, it should use the status code description
    exc = SanicException(status_code=200)
    expected_message = STATUS_CODES.get(200, b"").decode()
    assert exc.args[0] == expected_message
    assert exc.status_code == 200
    assert exc.message == expected_message

def test_sanic_exception_bytes_message_decoded():
    # Bytes message should be decoded to str
    raw = b"Binary error"
    exc = SanicException(raw, status_code=500)
    assert exc.args[0] == "Binary error"
    assert exc.message == "Binary error"
    assert exc.status_code == 500
