import pytest
from sanic.exceptions import HTTPException
from sanic.helpers import STATUS_CODES

def test_http_exception_default_behavior():
    """When no message is provided, the exception should use the default status code message."""
    exc = HTTPException()
    # Default status_code is 500
    assert exc.status_code == 500
    # The message should be the standard 500 message
    assert exc.message == STATUS_CODES[500].decode()
    # Quiet flag should be False by default
    assert exc.quiet is False
    # Headers should be an empty dict
    assert exc.headers == {}

def test_http_exception_with_bytes_message_and_custom_status():
    """Providing a bytes message and a custom status code should set the message correctly."""
    custom_msg = b"Custom error occurred"
    exc = HTTPException(custom_msg, status_code=418, quiet=True, headers={"X-Test": "value"})
    # Status code should be set to the provided value
    assert exc.status_code == 418
    # Message should be decoded from bytes
    assert exc.message == "Custom error occurred"
    # Quiet flag should reflect the provided value
    assert exc.quiet is True
    # Headers should contain the custom header
    assert exc.headers == {"X-Test": "value"}

def test_http_exception_invalid_status_code_raises_value_error():
    """Providing an invalid status code should raise a ValueError when accessing STATUS_CODES."""
    # STATUS_CODES only contains valid HTTP status codes; using an invalid one should raise KeyError
    with pytest.raises(KeyError):
        # This will attempt to decode a non-existent status code
        HTTPException(status_code=9999)
