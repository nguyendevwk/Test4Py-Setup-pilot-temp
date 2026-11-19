import pytest
from sanic.exceptions import ServiceUnavailable


def test_service_unavailable_default_properties():
    """ServiceUnavailable should default to status 503 and quiet=True."""
    exc = ServiceUnavailable()
    assert exc.status_code == 503
    assert exc.quiet is True
    # The default message should be None
    assert exc.message is None


def test_service_unavailable_with_message_and_headers():
    """Providing a message and custom headers should be reflected in the exception."""
    headers = {"Retry-After": "120", "X-Custom": "value"}
    exc = ServiceUnavailable("Service busy", headers=headers)
    assert exc.message == "Service busy"
    assert exc.headers == headers
    # Ensure quiet remains True unless explicitly overridden
    assert exc.quiet is True


def test_service_unavailable_invalid_headers_type():
    """Passing a non-dict type to headers should raise a TypeError."""
    with pytest.raises(TypeError):
        ServiceUnavailable(headers="not a dict")
