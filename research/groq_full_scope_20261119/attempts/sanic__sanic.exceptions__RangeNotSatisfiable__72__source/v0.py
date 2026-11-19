import pytest
from sanic.exceptions import RangeNotSatisfiable
from sanic.helpers import STATUS_CODES

class DummyRange:
    def __init__(self, total):
        self.total = total

def test_default_status_and_quiet():
    """RangeNotSatisfiable should default to status 416 and quiet=True."""
    exc = RangeNotSatisfiable()
    assert exc.status_code == 416
    assert exc.quiet is True
    # The default message should be the status description
    assert exc.message == STATUS_CODES[416]

def test_content_range_header_inclusion():
    """Providing a content_range should add a Content-Range header."""
    dummy = DummyRange(total=12345)
    exc = RangeNotSatisfiable(content_range=dummy)
    # The header should be present and correctly formatted
    assert "Content-Range" in exc.headers
    assert exc.headers["Content-Range"] == "bytes */12345"

def test_quiet_override_and_headers_preservation():
    """Explicit quiet flag should override default and existing headers should be preserved."""
    exc = RangeNotSatisfiable(quiet=False, headers={"X-Test": "value"})
    assert exc.quiet is False
    # Existing headers should remain unchanged
    assert exc.headers["X-Test"] == "value"
    # No Content-Range header should be added when content_range is None
    assert "Content-Range" not in exc.headers
