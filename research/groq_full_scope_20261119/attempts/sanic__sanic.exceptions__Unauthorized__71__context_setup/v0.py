import pytest
from sanic.exceptions import Unauthorized
from sanic.helpers import STATUS_CODES

def test_unauthorized_basic_challenge(tmp_path):
    """When a scheme and challenges are provided, the WWW-Authenticate header is set correctly."""
    exc = Unauthorized(
        "Auth required.",
        scheme="Basic",
        realm="Restricted Area",
        charset="UTF-8",
    )
    # The header should contain all challenge parameters in the order they were passed
    expected_header = 'Basic realm="Restricted Area", charset="UTF-8"'
    assert exc.headers["WWW-Authenticate"] == expected_header
    # The status code and quiet flag should be as defined on the class
    assert exc.status_code == 401
    assert exc.quiet is True
    # The message should be stored as a string
    assert exc.message == "Auth required."

def test_unauthorized_no_scheme_and_bytes_message():
    """If no scheme is given, the WWW-Authenticate header should not be added, and a bytes message is decoded."""
    raw_msg = b"Binary message"
    exc = Unauthorized(raw_msg)
    # No WWW-Authenticate header should be present
    assert "WWW-Authenticate" not in exc.headers
    # The message should be decoded to a string
    assert exc.message == "Binary message"
    # Default status code and quiet flag
    assert exc.status_code == 401
    assert exc.quiet is True

def test_unauthorized_default_message_from_status_code():
    """When message is None, the exception should use the standard status code message."""
    exc = Unauthorized(message=None)
    # STATUS_CODES contains the standard reason phrase for 401
    expected_msg = STATUS_CODES[401].decode()
    assert exc.message == expected_msg
    # The headers should still be empty (no scheme)
    assert exc.headers == {}
    # Quiet flag remains True
    assert exc.quiet is True
