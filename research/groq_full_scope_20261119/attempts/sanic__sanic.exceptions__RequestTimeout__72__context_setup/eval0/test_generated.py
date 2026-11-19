import pytest
from sanic.exceptions import RequestTimeout
from sanic.helpers import STATUS_CODES

def test_default_message_and_status():
    """RequestTimeout without arguments should use default status and message."""
    exc = RequestTimeout()
    # status_code should be 408
    assert exc.status_code == 408
    # default message should be the status description
    expected_msg = STATUS_CODES[408].decode()
    assert exc.message == expected_msg
    # quiet flag should be True as defined on the class
    assert exc.quiet is True
    # headers should be empty dict
    assert exc.headers == {}

def test_custom_message_and_headers():
    """Providing a custom message and headers should override defaults."""
    custom_msg = "Custom timeout message"
    custom_headers = {"X-Custom": "value"}
    exc = RequestTimeout(custom_msg, headers=custom_headers)
    # status_code remains 408
    assert exc.status_code == 408
    # message should be the custom string
    assert exc.message == custom_msg
    # quiet remains True
    assert exc.quiet is True
    # headers should match the provided dict
    assert exc.headers == custom_headers

def test_bytes_message_decoding():
    """Message passed as bytes should be decoded to string."""
    byte_msg = b"Byte message"
    exc = RequestTimeout(byte_msg)
    # message should be decoded string
    assert isinstance(exc.message, str)
    assert exc.message == "Byte message"
    # status_code remains 408
    assert exc.status_code == 408
