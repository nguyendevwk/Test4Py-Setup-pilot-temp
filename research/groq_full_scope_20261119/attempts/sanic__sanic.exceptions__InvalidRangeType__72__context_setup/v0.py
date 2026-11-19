import pytest
from sanic.exceptions import InvalidRangeType
from sanic.models.protocol_types import Range


def test_invalid_range_type_default_initialization():
    """When instantiated without arguments, the exception should have the
    correct status code, default message, and no custom headers."""
    exc = InvalidRangeType()
    assert isinstance(exc, InvalidRangeType)
    assert exc.status_code == 416
    # Default message is None, which means the HTTP status text will be used
    assert exc.message is None
    # No custom headers should be present
    assert exc.headers == {}
    # The quiet flag should be True by default
    assert exc.quiet is True


def test_invalid_range_type_with_content_range():
    """Providing a content_range should add a Content-Range header
    with the total size from the Range object."""
    # Create a simple Range object with a total of 1000 bytes
    class DummyRange:
        total = 1000

    dummy_range = DummyRange()
    exc = InvalidRangeType(content_range=dummy_range)
    assert exc.headers == {"Content-Range": "bytes */1000"}
    # The status code and quiet flag should remain unchanged
    assert exc.status_code == 416
    assert exc.quiet is True


def test_invalid_range_type_quiet_and_headers():
    """The quiet flag and custom headers should be respected when passed."""
    custom_headers = {"X-Custom": "value"}
    exc = InvalidRangeType(quiet=False, headers=custom_headers)
    # quiet flag should be overridden
    assert exc.quiet is False
    # Custom headers should be present
    assert exc.headers == custom_headers
    # Status code remains 416
    assert exc.status_code == 416
