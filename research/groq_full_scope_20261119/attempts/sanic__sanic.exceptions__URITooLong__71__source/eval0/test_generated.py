import pytest
from sanic.exceptions import URITooLong
from sanic.helpers import STATUS_CODES


def test_default_properties():
    """URITooLong should have the correct default status code and quiet flag."""
    exc = URITooLong()
    assert exc.status_code == 414
    assert exc.quiet is True
    # Default message should be the status description
    assert exc.message == STATUS_CODES[414]
    # No headers by default
    assert exc.headers == {}


def test_custom_message_and_headers():
    """Custom message and headers should be preserved."""
    custom_msg = "Custom URI too long error"
    custom_headers = {"X-Custom": "value"}
    exc = URITooLong(message=custom_msg, headers=custom_headers)
    assert exc.message == custom_msg
    assert exc.headers == custom_headers
    # The status code remains unchanged
    assert exc.status_code == 414
    # quiet flag remains default
    assert exc.quiet is True


def test_exception_raised_and_caught():
    """Raising URITooLong should propagate the correct exception."""
    try:
        raise URITooLong("Too long")
    except URITooLong as e:
        assert isinstance(e, URITooLong)
        assert e.message == "Too long"
        assert e.status_code == 414
        assert e.quiet is True
    else:
        pytest.fail("URITooLong was not raised")
