import pytest
from sanic.exceptions import HeaderNotFound
from sanic.helpers import STATUS_CODES

def test_header_not_found_default_message_and_status():
    """HeaderNotFound should default to status 400 and use the default message."""
    exc = HeaderNotFound()
    # Status code should be 400
    assert exc.status == 400
    # The default message should be the status phrase
    assert exc.message == STATUS_CODES[400]
    # No custom headers should be present
    assert exc.headers == {}

def test_header_not_found_with_custom_headers_and_context():
    """HeaderNotFound should store custom headers and context correctly."""
    custom_headers = {"X-Custom": "value"}
    context = {"detail": "missing header"}
    exc = HeaderNotFound(message="Missing header", headers=custom_headers, context=context)
    # Status code remains 400
    assert exc.status == 400
    # Custom message should be preserved
    assert exc.message == "Missing header"
    # Headers should be exactly the custom ones
    assert exc.headers == custom_headers
    # Context should be stored
    assert exc.context == context

def test_header_not_found_with_empty_headers_and_quiet_flag():
    """HeaderNotFound should handle empty headers and the quiet flag."""
    exc = HeaderNotFound(headers={}, quiet=True)
    # Status code should be 400
    assert exc.status == 400
    # Headers should be an empty dict
    assert exc.headers == {}
    # Quiet flag should be set
    assert exc.quiet is True
