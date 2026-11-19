import pytest
from sanic.exceptions import InvalidRangeType
from sanic.models.protocol_types import Range


def test_default_properties():
    """InvalidRangeType should expose the correct default status and quiet flag."""
    exc = InvalidRangeType()
    assert exc.status_code == 416
    assert exc.quiet is True
    # No custom message should default to None
    assert exc.args[0] is None
    # No headers should be set by default
    assert exc.headers == {}


def test_content_range_header_inclusion():
    """Providing a content_range should add a Content-Range header."""
    class DummyRange(Range):
        def __init__(self, total):
            self.total = total

    dummy = DummyRange(total=12345)
    exc = InvalidRangeType(content_range=dummy)
    # The header should reflect the total from the range
    assert exc.headers["Content-Range"] == "bytes */12345"
    # No other headers should be present
    assert set(exc.headers.keys()) == {"Content-Range"}


def test_custom_message_and_headers():
    """Custom message and headers should be preserved in the exception."""
    custom_msg = "Custom error message"
    custom_headers = {"X-Custom": "value"}
    exc = InvalidRangeType(custom_msg, headers=custom_headers)
    # The message should be stored in args[0]
    assert exc.args[0] == custom_msg
    # Custom headers should be merged with any default headers
    assert exc.headers["X-Custom"] == "value"
    # No Content-Range header should be present
    assert "Content-Range" not in exc.headers
