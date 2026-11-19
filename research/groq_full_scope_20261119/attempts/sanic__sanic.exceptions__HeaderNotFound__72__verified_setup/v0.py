import pytest
from sanic.exceptions import HeaderNotFound

# Test 1: Default construction – should default to status 400 and no message
def test_header_not_found_default():
    exc = HeaderNotFound()
    # Status code should be 400 (Bad Request)
    assert getattr(exc, "status", None) == 400
    # Default message should be None
    assert getattr(exc, "message", None) is None
    # No headers should be set by default
    assert getattr(exc, "headers", None) is None
    # quiet flag should be None by default
    assert getattr(exc, "quiet", None) is None

# Test 2: Custom message and headers – ensure they are stored correctly
def test_header_not_found_custom_message_and_headers():
    custom_msg = "Missing required header"
    custom_headers = {"X-Custom-Error": "True"}
    exc = HeaderNotFound(custom_msg, headers=custom_headers)
    # Status code remains 400
    assert exc.status == 400
    # Message should match the custom message
    assert exc.message == custom_msg
    # Headers should be exactly the custom headers dict
    assert exc.headers == custom_headers

# Test 3: Quiet flag – verify that the quiet attribute is set appropriately
def test_header_not_found_quiet_flag():
    exc = HeaderNotFound(quiet=True)
    # quiet flag should be True
    assert exc.quiet is True
    # Other attributes remain default
    assert exc.status == 400
    assert exc.message is None
    assert exc.headers is None
