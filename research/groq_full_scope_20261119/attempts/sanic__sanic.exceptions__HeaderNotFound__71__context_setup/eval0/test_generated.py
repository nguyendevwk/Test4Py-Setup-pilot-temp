import pytest
from sanic.exceptions import HeaderNotFound
from sanic.exceptions import BadRequest

def test_header_not_found_default_status_and_quiet():
    """HeaderNotFound should default to status 400 and quiet True."""
    exc = HeaderNotFound()
    assert isinstance(exc, BadRequest)
    assert exc.status_code == 400
    assert exc.quiet is True
    assert exc.message is None
    assert exc.headers is None

def test_header_not_found_custom_message_and_headers():
    """Custom message and headers should be stored correctly."""
    custom_msg = "Missing required header"
    custom_headers = {"X-Error": "HeaderMissing"}
    exc = HeaderNotFound(custom_msg, headers=custom_headers)
    assert exc.message == custom_msg
    assert exc.headers == custom_headers
    # quiet should remain default True unless overridden
    assert exc.quiet is True

def test_header_not_found_context_and_extra():
    """Context and extra data should be accessible via attributes."""
    ctx = {"field": "value"}
    extra = {"internal": "debug"}
    exc = HeaderNotFound("Error", context=ctx, extra=extra)
    assert exc.context == ctx
    assert exc.extra == extra
    # Ensure that context and extra are not None
    assert exc.context is not None
    assert exc.extra is not None
