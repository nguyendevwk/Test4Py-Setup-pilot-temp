import pytest
from sanic.exceptions import RangeNotSatisfiable
from sanic.helpers import STATUS_CODES


class DummyRange:
    """Simple object mimicking the Range protocol with a total attribute."""
    def __init__(self, total: int):
        self.total = total


def test_default_status_and_quiet():
    """RangeNotSatisfiable should have status code 416 and quiet set to True by default."""
    exc = RangeNotSatisfiable()
    assert exc.status_code == 416
    assert exc.quiet is True
    # The default message should be the status description
    assert exc.message == STATUS_CODES[416]


def test_content_range_header_inclusion():
    """Providing a content_range should add a Content-Range header with the total size."""
    total_size = 1024
    content_range = DummyRange(total=total_size)
    exc = RangeNotSatisfiable(content_range=content_range)
    # The header should be present and correctly formatted
    assert "Content-Range" in exc.headers
    assert exc.headers["Content-Range"] == f"bytes */{total_size}"


def test_custom_message_and_headers_override():
    """Custom message and headers should override defaults and be preserved."""
    custom_msg = "Custom error message"
    custom_headers = {"X-Custom-Header": "value"}
    exc = RangeNotSatisfiable(
        message=custom_msg,
        headers=custom_headers,
        content_range=DummyRange(total=500),
    )
    # Message should be the custom one
    assert exc.message == custom_msg
    # Custom header should be present
    assert exc.headers["X-Custom-Header"] == "value"
    # Content-Range header should also be present
    assert exc.headers["Content-Range"] == "bytes */500"
