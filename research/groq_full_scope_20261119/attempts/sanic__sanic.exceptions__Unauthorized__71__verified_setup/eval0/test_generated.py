import pytest
from sanic.exceptions import Unauthorized


def test_unauthorized_with_scheme_and_challenges(tmp_path):
    """When a scheme and challenges are provided, the WWW-Authenticate header
    should be constructed correctly and the instance should carry the
    provided message."""
    exc = Unauthorized(
        "Auth required.",
        scheme="Basic",
        realm="Restricted Area",
        charset="UTF-8",
    )
    # status code and quiet default
    assert exc.status_code == 401
    assert exc.quiet is True
    # message stored
    assert exc.message == "Auth required."
    # WWW-Authenticate header should contain all key/value pairs
    header = exc.headers.get("WWW-Authenticate")
    assert header is not None
    # order of items is not guaranteed, but all should be present
    assert 'Basic' in header
    assert 'realm="Restricted Area"' in header
    assert 'charset="UTF-8"' in header
    # No trailing comma or space
    assert not header.endswith(",")
    assert not header.endswith(" ")


def test_unauthorized_without_scheme(tmp_path):
    """When no scheme is provided, no WWW-Authenticate header should be added."""
    exc = Unauthorized("No auth needed.")
    # headers should be empty or not contain WWW-Authenticate
    assert "WWW-Authenticate" not in exc.headers
    # message stored
    assert exc.message == "No auth needed."
    # quiet default
    assert exc.quiet is True


def test_unauthorized_headers_override_and_extra(tmp_path):
    """Headers passed to the constructor should be merged with the
    automatically added WWW-Authenticate header, and extra data should
    not appear in the public headers."""
    exc = Unauthorized(
        "Token missing",
        scheme="Bearer",
        headers={"X-Custom": "value"},
        extra={"internal": "secret"},
    )
    # Custom header preserved
    assert exc.headers["X-Custom"] == "value"
    # WWW-Authenticate header present
    assert exc.headers["WWW-Authenticate"] == "Bearer"
    # Extra data should not be in headers
    assert "internal" not in exc.headers
    # The internal extra dict should be stored separately
    assert exc.extra == {"internal": "secret"}
