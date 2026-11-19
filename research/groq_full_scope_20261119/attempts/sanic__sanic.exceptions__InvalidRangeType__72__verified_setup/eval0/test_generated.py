import pytest
from sanic.exceptions import InvalidRangeType
from sanic.models.protocol_types import Range


def test_invalid_range_type_basic_attributes():
    """Normal instantiation should set status_code, quiet, and store message."""
    exc = InvalidRangeType(message="Test message")
    assert isinstance(exc, InvalidRangeType)
    assert exc.status_code == 416
    assert exc.quiet is True
    # The message should be accessible via the args of the exception
    assert exc.args[0] == "Test message"


def test_invalid_range_type_with_content_range_and_headers():
    """Providing a Range and custom headers should store them on the instance."""
    rng = Range(0, 100)
    headers = {"X-Custom": "value"}
    exc = InvalidRangeType(message="Range error", content_range=rng, headers=headers)
    # The content_range should be stored
    assert getattr(exc, "content_range", None) == rng
    # Headers should be stored
    assert getattr(exc, "headers", None) == headers
    # Message should still be accessible
    assert exc.args[0] == "Range error"


def test_invalid_range_type_invalid_content_range_type():
    """Passing a non-Range object for content_range should raise a TypeError."""
    with pytest.raises(TypeError):
        InvalidRangeType(message="Bad range", content_range="not a Range")
