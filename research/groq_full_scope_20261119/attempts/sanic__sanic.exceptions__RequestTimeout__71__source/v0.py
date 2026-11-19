import pytest
from sanic.exceptions import RequestTimeout
from sanic.helpers import STATUS_CODES

def test_default_properties():
    """RequestTimeout should have default status code and quiet flag."""
    exc = RequestTimeout()
    assert exc.status_code == 408
    assert exc.quiet is True
    # The default message should be the status description
    assert exc.message == STATUS_CODES[408]

def test_custom_message_and_headers():
    """Custom message and headers are stored correctly."""
    custom_msg = "Custom timeout message"
    custom_headers = {"Retry-After": "120"}
    exc = RequestTimeout(message=custom_msg, headers=custom_headers)
    assert exc.message == custom_msg
    assert exc.headers == custom_headers
    # Ensure quiet remains True unless explicitly overridden
    assert exc.quiet is True

def test_error_in_production_mode():
    """When in production mode, extra context should not be exposed."""
    exc = RequestTimeout(message="prod message", extra={"secret": "data"})
    # In production, the extra dict should not be part of the public data
    # The HTTPException base class exposes a `data` attribute for public payload
    # which should not contain the 'extra' key.
    public_data = getattr(exc, "data", {})
    assert "secret" not in public_data
    # However, the internal `_extra` attribute should still hold the data
    assert getattr(exc, "_extra", None) == {"secret": "data"}
