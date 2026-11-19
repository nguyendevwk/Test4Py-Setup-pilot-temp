import pytest
from sanic.exceptions import URITooLong


def test_default_attributes():
    """URITooLong should have the correct default status code and quiet flag."""
    exc = URITooLong()
    assert exc.status_code == 414
    assert exc.quiet is True
    # Default message should be None, which will be replaced by the status text
    assert exc.message is None
    # No headers by default
    assert getattr(exc, "headers", None) is None


def test_custom_message_and_headers():
    """Providing a custom message and headers should store them correctly."""
    custom_msg = "Custom URI too long error"
    custom_headers = {"X-Custom": "value"}
    exc = URITooLong(custom_msg, headers=custom_headers)
    # The message should be stored as provided
    assert exc.message == custom_msg
    # Headers should be accessible via the headers attribute
    assert exc.headers == custom_headers
    # Quiet flag remains True unless overridden
    assert exc.quiet is True


def test_quiet_flag_override_and_context():
    """The quiet flag can be overridden and context should be stored."""
    exc = URITooLong(quiet=False, context={"detail": "extra info"})
    # Quiet flag should reflect the overridden value
    assert exc.quiet is False
    # Context should be stored on the exception
    assert exc.context == {"detail": "extra info"}
    # The status code remains unchanged
    assert exc.status_code == 414
