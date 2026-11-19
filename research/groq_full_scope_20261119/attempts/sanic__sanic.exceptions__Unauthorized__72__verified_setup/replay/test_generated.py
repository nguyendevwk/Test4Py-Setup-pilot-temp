import pytest
from sanic.exceptions import Unauthorized


def test_unauthorized_with_scheme_and_challenges(tmp_path):
    """When a scheme and challenges are provided, the WWW-Authenticate header
    should be constructed correctly and merged with any custom headers."""
    exc = Unauthorized(
        "Auth required.",
        scheme="Basic",
        realm="Restricted Area",
        charset="UTF-8",
        headers={"X-Custom": "value"},
    )
    # The status code should be 401
    assert exc.status_code == 401
    # The message should be stored
    assert exc.message == "Auth required."
    # The custom header should be present
    assert exc.headers["X-Custom"] == "value"
    # The WWW-Authenticate header should contain all challenge params
    expected = 'Basic realm="Restricted Area", charset="UTF-8"'
    assert exc.headers["WWW-Authenticate"] == expected


def test_unauthorized_without_scheme(tmp_path):
    """When no scheme is provided, no WWW-Authenticate header should be added."""
    exc = Unauthorized("No auth needed.")
    # No WWW-Authenticate header should exist
    assert "WWW-Authenticate" not in exc.headers
    # The quiet flag should default to True as defined on the class
    assert exc.quiet is True
    # The status code remains 401
    assert exc.status_code == 401
    # The message should be stored
    assert exc.message == "No auth needed."


def test_unauthorized_invalid_challenge_value(tmp_path):
    """Challenge values can be any type; they are converted to string."""
    exc = Unauthorized(
        "Invalid challenge",
        scheme="Bearer",
        token_type=123,  # non-string value
        realm=None,      # None value should be converted to 'None'
    )
    # The challenge string should include the string representations
    # of the values, even if they are not strings.
    expected = 'Bearer token_type="123", realm="None"'
    assert exc.headers["WWW-Authenticate"] == expected
    # Ensure that the exception still has the correct status code
    assert exc.status_code == 401
