import pytest
from sanic.exceptions import RequestTimeout


def test_default_initialization():
    """RequestTimeout should initialize with default attributes."""
    exc = RequestTimeout()
    # Default status code
    assert exc.status_code == 408
    # Default quiet flag
    assert exc.quiet is True
    # No message by default
    assert exc.message is None
    # No headers or context
    assert exc.headers == {}
    assert exc.context == {}
    # Extra should be empty dict
    assert exc.extra == {}


def test_custom_headers_and_context():
    """Custom headers and context should be stored correctly."""
    headers = {"X-Custom": "value"}
    context = {"detail": "timeout occurred"}
    exc = RequestTimeout(
        message="Timed out",
        headers=headers,
        context=context,
    )
    # Message should be stored
    assert exc.message == "Timed out"
    # Headers should be exactly as provided
    assert exc.headers == headers
    # Context should be exactly as provided
    assert exc.context == context
    # Quiet flag remains default True unless overridden
    assert exc.quiet is True
    # Extra remains empty
    assert exc.extra == {}


def test_status_code_and_quiet_override():
    """Status code is fixed and quiet can be overridden."""
    exc = RequestTimeout(quiet=False)
    # Status code remains 408
    assert exc.status_code == 408
    # Quiet flag overridden
    assert exc.quiet is False
    # No message
    assert exc.message is None
