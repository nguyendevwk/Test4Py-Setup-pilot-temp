import pytest
from sanic.exceptions import Unauthorized

def test_default_unauthorized_attributes():
    """Unauthorized without arguments should have status 401, quiet True and no WWW-Authenticate header."""
    exc = Unauthorized()
    assert exc.status_code == 401
    assert exc.quiet is True
    # No custom headers set
    assert exc.headers == {}
    # No WWW-Authenticate header
    assert "WWW-Authenticate" not in exc.headers

def test_unauthorized_with_scheme_and_challenges():
    """Providing a scheme and challenge parameters should set the correct WWW-Authenticate header."""
    exc = Unauthorized(
        "Auth required.",
        scheme="Basic",
        realm="Restricted Area",
        charset="UTF-8"
    )
    # The header should include all challenge parameters in the order provided
    expected_header = 'Basic realm="Restricted Area", charset="UTF-8"'
    assert exc.headers["WWW-Authenticate"] == expected_header
    # The original message should be preserved
    assert exc.message == "Auth required."

def test_unauthorized_quiet_override_and_extra_headers():
    """Quiet flag can be overridden and additional headers are merged correctly."""
    exc = Unauthorized(
        "Forbidden",
        scheme="Bearer",
        quiet=False,
        headers={"X-Custom": "value"},
        realm="API"
    )
    # quiet should reflect the overridden value
    assert exc.quiet is False
    # Additional headers should be merged
    assert exc.headers["X-Custom"] == "value"
    # WWW-Authenticate header should include the scheme and challenge
    assert exc.headers["WWW-Authenticate"] == 'Bearer realm="API"'
