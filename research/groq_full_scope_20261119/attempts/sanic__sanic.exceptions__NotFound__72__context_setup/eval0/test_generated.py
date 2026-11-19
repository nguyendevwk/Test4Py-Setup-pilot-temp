import pytest
from sanic.exceptions import NotFound
from sanic.helpers import STATUS_CODES


def test_default_not_found_message_and_status():
    """When no message is supplied, the exception should use the default
    status code 404 and the corresponding status text from STATUS_CODES."""
    exc = NotFound()
    assert exc.status_code == 404
    # STATUS_CODES maps 404 to b"Not Found"
    assert exc.message == STATUS_CODES[404].decode()
    # quiet should default to the class value
    assert exc.quiet is True
    # headers should be the class default (empty dict)
    assert exc.headers == {}


def test_not_found_with_bytes_message():
    """Providing a bytes message should be decoded to a string."""
    raw_msg = b"Resource missing"
    exc = NotFound(raw_msg)
    assert exc.message == "Resource missing"
    assert exc.status_code == 404
    # quiet remains True
    assert exc.quiet is True


def test_not_found_custom_headers_and_quiet():
    """Custom headers and quiet flag should override class defaults."""
    custom_headers = {"X-Custom": "value"}
    exc = NotFound(quiet=False, headers=custom_headers)
    assert exc.headers == custom_headers
    assert exc.quiet is False
    # status code and message remain default
    assert exc.status_code == 404
    assert exc.message == STATUS_CODES[404].decode()
