import pytest
from sanic.exceptions import RangeNotSatisfiable
from sanic.models.protocol_types import Range


class DummyRange:
    """Simple mock of the Range protocol with a total attribute."""
    def __init__(self, total: int):
        self.total = total


def test_default_initialization():
    """RangeNotSatisfiable should set status_code, quiet, and default headers."""
    exc = RangeNotSatisfiable()
    assert exc.status_code == 416
    assert exc.quiet is True
    # No custom headers should be present
    assert exc.headers == {}
    # Default message should be the status description
    assert exc.message == "Range Not Satisfiable"


def test_content_range_header_inclusion():
    """Providing a content_range should add the correct Content-Range header."""
    dummy = DummyRange(total=12345)
    exc = RangeNotSatisfiable(content_range=dummy)
    assert exc.headers["Content-Range"] == "bytes */12345"
    # Ensure other headers remain unchanged
    assert len(exc.headers) == 1


def test_custom_message_and_headers():
    """Custom message and headers should override defaults correctly."""
    custom_headers = {"X-Custom": "value"}
    exc = RangeNotSatisfiable(
        message="Custom error",
        headers=custom_headers,
    )
    assert exc.message == "Custom error"
    assert exc.headers == custom_headers
    # quiet should remain True unless explicitly overridden
    assert exc.quiet is True
