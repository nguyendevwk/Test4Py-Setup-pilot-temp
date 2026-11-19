import pytest
from sanic.exceptions import RangeNotSatisfiable
from sanic.models.protocol_types import Range


class DummyRange:
    """Simple object mimicking the Range protocol with a `total` attribute."""
    def __init__(self, total: int):
        self.total = total


def test_default_status_and_quiet():
    """RangeNotSatisfiable should default to status 416 and quiet=True."""
    exc = RangeNotSatisfiable()
    assert exc.status_code == 416
    assert exc.quiet is True
    # No custom headers should be present
    assert exc.headers == {}


def test_content_range_header_inclusion():
    """Providing a content_range should add the correct Content-Range header."""
    dummy = DummyRange(total=1024)
    exc = RangeNotSatisfiable(content_range=dummy)
    assert exc.headers["Content-Range"] == "bytes */1024"
    # Ensure other headers remain unchanged
    assert len(exc.headers) == 1


def test_custom_headers_merge_and_overwrite():
    """Custom headers should merge with the Content-Range header and override if duplicate."""
    dummy = DummyRange(total=2048)
    custom = {"Content-Range": "bytes */9999", "X-Custom": "value"}
    exc = RangeNotSatisfiable(content_range=dummy, headers=custom)
    # Content-Range should be overridden by the custom value
    assert exc.headers["Content-Range"] == "bytes */9999"
    assert exc.headers["X-Custom"] == "value"
    # No other unexpected headers
    assert set(exc.headers.keys()) == {"Content-Range", "X-Custom"}
