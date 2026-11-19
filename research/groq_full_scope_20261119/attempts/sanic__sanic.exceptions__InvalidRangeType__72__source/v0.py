import pytest
from sanic.exceptions import InvalidRangeType


def test_default_invalid_range_type_attributes():
    """Verify default attributes of InvalidRangeType."""
    exc = InvalidRangeType()
    # Status code should be 416
    assert exc.status_code == 416
    # quiet flag should be True by default
    assert exc.quiet is True
    # message should be None when not provided
    assert exc.message is None
    # headers should be None by default
    assert exc.headers is None
    # context and extra should be None by default
    assert exc.context is None
    assert exc.extra is None


def test_invalid_range_type_with_message_and_headers():
    """Verify that custom message and headers are stored correctly."""
    custom_msg = "Invalid range requested"
    custom_headers = {"X-Custom-Header": "value"}
    exc = InvalidRangeType(message=custom_msg, headers=custom_headers)
    assert exc.message == custom_msg
    assert exc.headers == custom_headers
    # status_code and quiet remain unchanged
    assert exc.status_code == 416
    assert exc.quiet is True


def test_invalid_range_type_context_and_extra():
    """Verify that context and extra data are preserved."""
    context_data = {"user_id": 123}
    extra_data = {"debug": True}
    exc = InvalidRangeType(context=context_data, extra=extra_data)
    assert exc.context == context_data
    assert exc.extra == extra_data
    # Ensure that the exception can be raised and caught without error
    with pytest.raises(InvalidRangeType):
        raise exc
