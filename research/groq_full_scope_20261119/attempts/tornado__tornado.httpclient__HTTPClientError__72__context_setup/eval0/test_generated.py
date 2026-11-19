import pytest
from tornado.httpclient import HTTPClientError, httputil


def test_httpclienterror_default_message_and_repr():
    """Verify that the default message comes from httputil.responses
    and that __repr__ equals __str__."""
    # Use a known HTTP status code that exists in httputil.responses
    error = HTTPClientError(404)
    assert error.code == 404
    assert error.message == httputil.responses[404]
    assert error.response is None
    expected_str = f"HTTP 404: {httputil.responses[404]}"
    assert str(error) == expected_str
    # __repr__ is aliased to __str__
    assert repr(error) == expected_str


def test_httpclienterror_unknown_code_and_custom_message():
    """Verify that an unknown status code uses 'Unknown' and that a custom
    message overrides the default."""
    # 999 is not a standard HTTP status code
    error = HTTPClientError(999, message="Custom error")
    assert error.code == 999
    assert error.message == "Custom error"
    assert error.response is None
    assert str(error) == "HTTP 999: Custom error"


def test_httpclienterror_with_response_object():
    """Verify that passing a response object stores it correctly."""
    class DummyResponse:
        def __init__(self, body):
            self.body = body

    dummy = DummyResponse(body=b"test")
    error = HTTPClientError(500, response=dummy)
    assert error.code == 500
    assert error.message == httputil.responses[500]
    assert error.response is dummy
    # The string representation should not include the response object
    assert "test" not in str(error)
