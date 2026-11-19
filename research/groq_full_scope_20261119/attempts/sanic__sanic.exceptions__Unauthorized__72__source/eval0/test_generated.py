import pytest
from sanic.exceptions import Unauthorized

def test_default_unauthorized_initialization():
    """Unauthorized should default to status 401, quiet True, and no WWW-Authenticate header."""
    exc = Unauthorized()
    assert exc.status_code == 401
    assert exc.quiet is True
    # No message means default message is used by HTTPException (not checked here)
    assert exc.message is None
    # No scheme means no WWW-Authenticate header
    assert "WWW-Authenticate" not in exc.headers

def test_unauthorized_with_scheme_and_challenges():
    """Providing a scheme and challenges should construct the correct WWW-Authenticate header."""
    exc = Unauthorized(
        "Auth required.",
        scheme="Basic",
        realm="Restricted Area",
        charset="UTF-8"
    )
    # Status and quiet should remain unchanged
    assert exc.status_code == 401
    assert exc.quiet is True
    # Message should be stored
    assert exc.message == "Auth required."
    # WWW-Authenticate header should include scheme and all challenges
    expected_header = 'Basic realm="Restricted Area", charset="UTF-8"'
    assert exc.headers["WWW-Authenticate"] == expected_header

def test_unauthorized_with_bytes_message_and_no_scheme():
    """Message can be bytes and no scheme should not add WWW-Authenticate header."""
    exc = Unauthorized(b"Binary message")
    assert exc.message == b"Binary message"
    assert "WWW-Authenticate" not in exc.headers
