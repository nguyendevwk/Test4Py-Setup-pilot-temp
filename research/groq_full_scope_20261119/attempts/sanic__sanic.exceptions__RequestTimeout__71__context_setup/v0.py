import pytest
from sanic.exceptions import RequestTimeout
from sanic.helpers import STATUS_CODES


def test_default_message_and_status():
    """RequestTimeout without arguments should use default status and message."""
    exc = RequestTimeout()
    # status_code should be 408
    assert exc.status_code == 408
    # quiet should be True as defined on the class
    assert exc.quiet is True
    # message should be the default status message for 408
    expected_msg = STATUS_CODES[408].decode()
    assert exc.message == expected_msg
    # headers should be empty dict
    assert exc.headers == {}


def test_custom_message_and_headers():
    """Providing a custom message and headers should override defaults."""
    custom_msg = "Custom timeout occurred"
    custom_headers = {"X-Custom": "value"}
    exc = RequestTimeout(custom_msg, headers=custom_headers)
    # status_code remains 408
    assert exc.status_code == 408
    # quiet remains True
    assert exc.quiet is True
    # message should be the custom string
    assert exc.message == custom_msg
    # headers should match the provided dict
    assert exc.headers == custom_headers


def test_status_code_and_quiet_explicit():
    """Explicitly setting status_code and quiet should override class defaults."""
    # Use a different status code to see the effect
    class CustomTimeout(RequestTimeout):
        status_code = 499
        quiet = False

    exc = CustomTimeout()
    # status_code should be overridden by the subclass
    assert exc.status_code == 499
    # quiet should be overridden by the subclass
    assert exc.quiet is False
    # message should be the default for 499
    expected_msg = STATUS_CODES[499].decode()
    assert exc.message == expected_msg
