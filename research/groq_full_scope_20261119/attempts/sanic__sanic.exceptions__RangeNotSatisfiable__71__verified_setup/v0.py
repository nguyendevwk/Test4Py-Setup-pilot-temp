import pytest
from sanic.exceptions import RangeNotSatisfiable
from sanic.models.protocol_types import Range


class DummyRange(Range):
    """Simple implementation of the Range protocol for testing."""
    def __init__(self, total: int):
        self.total = total


def test_default_initialization():
    """RangeNotSatisfiable should set status_code and quiet correctly when no arguments are provided."""
    exc = RangeNotSatisfiable()
    assert exc.status_code == 416
    assert exc.quiet is True
    # No custom headers should be added
    assert "Content-Range" not in exc.headers
    # Default message should be the status description
    assert exc.message == "Range Not Satisfiable"


def test_with_content_range_header():
    """Providing a content_range should add the correct Content-Range header."""
    dummy = DummyRange(total=12345)
    exc = RangeNotSatisfiable(content_range=dummy)
    assert exc.headers["Content-Range"] == "bytes */12345"
    # Ensure other headers are preserved (empty by default)
    assert len(exc.headers) == 1


def test_quiet_flag_and_custom_message():
    """The quiet flag should override the default and a custom message should be stored."""
    exc = RangeNotSatisfiable(message="Custom error", quiet=False)
    assert exc.quiet is False
    assert exc.message == "Custom error"
    # No Content-Range header when not provided
    assert "Content-Range" not in exc.headers
