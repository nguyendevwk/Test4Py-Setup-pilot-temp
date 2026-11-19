import pytest
from sanic.exceptions import InvalidRangeType
from sanic.models.protocol_types import Range


def test_default_initialization(tmp_path):
    """Instantiate with no arguments and verify default attributes."""
    exc = InvalidRangeType()
    # status_code should be 416
    assert exc.status_code == 416
    # quiet should default to True as defined in the class
    assert exc.quiet is True
    # message should be None when not provided
    assert exc.message is None
    # content_range should be None when not provided
    assert exc.content_range is None
    # headers should be None when not provided
    assert exc.headers is None
    # context and extra should be None
    assert exc.context is None
    assert exc.extra is None


def test_custom_message_and_headers(tmp_path):
    """Provide a custom message and headers and verify they are stored."""
    custom_msg = "Invalid range specified"
    custom_headers = {"X-Custom-Header": "value"}
    exc = InvalidRangeType(message=custom_msg, headers=custom_headers)
    assert exc.message == custom_msg
    assert exc.headers == custom_headers
    # quiet remains default True unless overridden
    assert exc.quiet is True
    # status_code remains 416
    assert exc.status_code == 416


def test_quiet_override_and_content_range(tmp_path):
    """Override quiet flag and provide a content_range object."""
    # Create a simple Range object (start=0, end=99, total=200)
    rng = Range(0, 99, 200)
    exc = InvalidRangeType(content_range=rng, quiet=False)
    assert exc.content_range == rng
    assert exc.quiet is False
    # message should still be None
    assert exc.message is None
    # headers should be None
    assert exc.headers is None
