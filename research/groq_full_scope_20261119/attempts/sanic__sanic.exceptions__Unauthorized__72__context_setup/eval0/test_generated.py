import pytest
from sanic.exceptions import Unauthorized


def test_unauthorized_basic_auth_header(tmp_path):
    """When a scheme and challenges are provided, the WWW-Authenticate header
    should contain all key/value pairs formatted correctly."""
    exc = Unauthorized(
        "Auth required.",
        scheme="Basic",
        realm="Restricted Area",
        charset="UTF-8",
    )
    # The header should start with the scheme and include all challenges
    header = exc.headers.get("WWW-Authenticate")
    assert header is not None
    assert header.startswith("Basic ")
    # Each challenge should be quoted and comma separated
    for key, value in {"realm": "Restricted Area", "charset": "UTF-8"}.items():
        assert f'{key}="{value}"' in header
    # The header should not end with a trailing comma or space
    assert not header.endswith(",") and not header.endswith(" ")


def test_unauthorized_message_bytes_decoded():
    """If the message is provided as bytes, it should be decoded to a string."""
    exc = Unauthorized(b"Binary message")
    # The exception's message attribute should be a decoded string
    assert isinstance(exc.message, str)
    assert exc.message == "Binary message"
    # The exception's string representation should also be the decoded message
    assert str(exc) == "Binary message"


def test_unauthorized_no_scheme_no_header(tmp_path):
    """When no scheme is provided, the WWW-Authenticate header should not be set."""
    exc = Unauthorized("No auth needed")
    # The headers dict should not contain the WWW-Authenticate key
    assert "WWW-Authenticate" not in exc.headers
    # The status code should be the default for Unauthorized
    assert exc.status_code == 401
    # The quiet flag should be True as defined on the class
    assert exc.quiet is True
