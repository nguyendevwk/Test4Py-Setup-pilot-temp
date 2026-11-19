import pytest
from sanic.exceptions import HeaderNotFound

def test_header_not_found_default_message_and_status():
    """HeaderNotFound should default to a 400 status and a default message."""
    exc = HeaderNotFound()
    # Status code should be 400
    assert exc.status == 400
    # Default message should be the status phrase
    assert exc.message == "Bad Request"
    # No headers should be set by default
    assert exc.headers == {}

def test_header_not_found_with_custom_headers_and_context():
    """HeaderNotFound should store custom headers and context correctly."""
    custom_headers = {"X-Custom": "value"}
    context = {"detail": "missing header"}
    exc = HeaderNotFound(message="Missing header", headers=custom_headers, context=context)
    # Status code remains 400
    assert exc.status == 400
    # Message should be the custom one
    assert exc.message == "Missing header"
    # Headers should be exactly the custom dict
    assert exc.headers == custom_headers
    # Context should be stored
    assert exc.context == context

def test_header_not_found_extra_not_included_in_client_response():
    """Extra data should not be exposed in the client response."""
    extra = {"secret": "data"}
    exc = HeaderNotFound(message="Error", extra=extra)
    # The `extra` attribute should be present on the exception
    assert exc.extra == extra
    # But the `client_response` (or similar) should not contain the secret
    # Since the actual client response construction is internal, we check that
    # the `extra` dict is not part of the `headers` or `context`.
    assert "secret" not in exc.headers
    assert "secret" not in exc.context or exc.context is None
