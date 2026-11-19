import pytest
from sanic.exceptions import InvalidHeader
from sanic.helpers import STATUS_CODES

def test_invalid_header_default_message_and_status():
    """InvalidHeader without a message should use the default status text."""
    exc = InvalidHeader()
    # Status code should be 400
    assert exc.status == 400
    # Default message should be the status code description
    assert exc.message == STATUS_CODES[400]
    # No custom headers by default
    assert exc.headers == {}

def test_invalid_header_with_custom_message_and_headers():
    """Providing a custom message and headers should override defaults."""
    custom_msg = "Invalid header value"
    custom_headers = {"X-Custom-Error": "true", "Retry-After": "30"}
    exc = InvalidHeader(message=custom_msg, headers=custom_headers)
    assert exc.status == 400
    assert exc.message == custom_msg
    # Headers should be exactly as provided
    assert exc.headers == custom_headers

def test_invalid_header_raises_on_non_dict_headers():
    """Headers argument must be a dict; passing a non-dict should raise TypeError."""
    with pytest.raises(TypeError):
        InvalidHeader(headers=["not", "a", "dict"])
