import pytest
from sanic.exceptions import ServiceUnavailable


def test_service_unavailable_basic_message_and_status():
    """Instantiate with a string message and verify status code and attributes."""
    exc = ServiceUnavailable("Service temporarily down")
    assert exc.status_code == 503
    assert exc.message == "Service temporarily down"
    assert exc.headers is None
    assert exc.quiet is True
    # The exception should be an instance of ServiceUnavailable
    assert isinstance(exc, ServiceUnavailable)


def test_service_unavailable_bytes_message_and_headers():
    """Instantiate with a bytes message and custom headers; verify attributes."""
    headers = {"Retry-After": "120"}
    exc = ServiceUnavailable(b"Service temporarily down", headers=headers)
    assert exc.status_code == 503
    assert exc.message == b"Service temporarily down"
    assert exc.headers == headers
    assert exc.quiet is True
    # Ensure the headers are preserved as provided
    assert exc.headers["Retry-After"] == "120"


def test_service_unavailable_invalid_headers_type_raises():
    """Passing a non-dict type for headers should raise a TypeError."""
    with pytest.raises(TypeError):
        ServiceUnavailable("Error", headers=["not", "a", "dict"])
