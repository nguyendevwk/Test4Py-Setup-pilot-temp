import pytest
from http.cookiejar import Cookie
from httpie.sessions import materialize_cookie, KEPT_COOKIE_OPTIONS


def test_materialize_cookie_basic_attributes():
    """Verify that all kept options are present and correctly copied."""
    cookie = Cookie(
        version=0,
        name="sessionid",
        value="abc123",
        port=None,
        port_specified=False,
        domain="example.com",
        domain_specified=True,
        domain_initial_dot=False,
        path="/",
        path_specified=True,
        secure=False,
        expires=0,
        discard=False,
        comment=None,
        comment_url=None,
        rest={},
        rfc2109=False,
    )
    result = materialize_cookie(cookie)
    # All KEPT_COOKIE_OPTIONS must be present
    assert set(result.keys()) == set(KEPT_COOKIE_OPTIONS)
    # Values should match the original cookie
    assert result["name"] == "sessionid"
    assert result["value"] == "abc123"
    assert result["domain"] == "example.com"
    assert result["path"] == "/"
    assert result["secure"] is False
    assert result["expires"] == 0


def test_materialize_cookie_explicit_none_domain():
    """When a cookie has an empty domain and the rest flag is_explicit_none,
    the domain should be converted to None."""
    cookie = Cookie(
        version=0,
        name="token",
        value="xyz",
        port=None,
        port_specified=False,
        domain="",
        domain_specified=True,
        domain_initial_dot=False,
        path="/",
        path_specified=True,
        secure=True,
        expires=0,
        discard=False,
        comment=None,
        comment_url=None,
        rest={"is_explicit_none": True},
        rfc2109=False,
    )
    result = materialize_cookie(cookie)
    assert result["domain"] is None
    assert result["secure"] is True
    assert result["name"] == "token"


def test_materialize_cookie_invalid_input_raises():
    """Passing an object that is not a Cookie should raise an AttributeError."""
    with pytest.raises(AttributeError):
        materialize_cookie(42)
