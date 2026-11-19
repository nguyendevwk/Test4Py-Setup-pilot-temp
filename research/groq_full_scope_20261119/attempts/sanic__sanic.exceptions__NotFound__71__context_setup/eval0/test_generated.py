import pytest
from sanic.exceptions import NotFound
from sanic.helpers import STATUS_CODES


def test_notfound_default_message_and_status():
    """When no message is provided, the default status message is used."""
    exc = NotFound()
    # Default status code should be 404
    assert exc.status_code == 404
    # Default message should be the standard HTTP status message for 404
    expected_msg = STATUS_CODES[404].decode()
    assert exc.args[0] == expected_msg
    # quiet flag should be True as defined on the class
    assert exc.quiet is True
    # No headers should be present by default
    assert exc.headers == {}


def test_notfound_custom_message_and_headers():
    """Providing a custom message and headers should override defaults."""
    custom_msg = "Resource missing"
    custom_headers = {"X-Custom": "value"}
    exc = NotFound(custom_msg, headers=custom_headers)
    # Status code remains 404
    assert exc.status_code == 404
    # Message should be the custom one
    assert exc.args[0] == custom_msg
    # Headers should include the custom header
    assert exc.headers == custom_headers
    # quiet flag remains True
    assert exc.quiet is True


def test_notfound_bytes_message_and_quiet_flag():
    """Bytes message should be decoded and quiet flag can be overridden."""
    exc = NotFound(b"Binary message", quiet=False)
    # Message should be decoded from bytes
    assert exc.args[0] == "Binary message"
    # quiet flag should reflect the passed value
    assert exc.quiet is False
    # Status code remains 404
    assert exc.status_code == 404
