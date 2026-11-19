import pytest
from http.cookiejar import Cookie
from httpie.sessions import materialize_cookie


def test_materialize_cookie_explicit_none_domain():
    # Cookie with empty domain and explicit_none flag should have domain set to None
    cookie = Cookie(
        version=0,
        name="session",
        value="abc123",
        port=None,
        port_specified=False,
        domain="",
        domain_specified=True,
        domain_initial_dot=False,
        path="/",
        path_specified=True,
        secure=False,
        expires=None,
        discard=True,
        comment=None,
        comment_url=None,
        rest={"is_explicit_none": True},
        rfc2109=False,
    )
    result = materialize_cookie(cookie)
    assert result["domain"] is None
    assert result["name"] == "session"
    assert result["value"] == "abc123"


def test_materialize_cookie_regular_domain():
    # Cookie with a normal domain should keep its domain value
    cookie = Cookie(
        version=0,
        name="token",
        value="xyz",
        port=None,
        port_specified=False,
        domain="example.com",
        domain_specified=True,
        domain_initial_dot=False,
        path="/",
        path_specified=True,
        secure=False,
        expires=None,
        discard=True,
        comment=None,
        comment_url=None,
        rest={},
        rfc2109=False,
    )
    result = materialize_cookie(cookie)
    assert result["domain"] == "example.com"
    assert result["name"] == "token"
    assert result["value"] == "xyz"


def test_materialize_cookie_no_rest_explicit_none():
    # Cookie with empty rest dict should not alter domain even if empty
    cookie = Cookie(
        version=0,
        name="id",
        value="123",
        port=None,
        port_specified=False,
        domain="",
        domain_specified=True,
        domain_initial_dot=False,
        path="/",
        path_specified=True,
        secure=False,
        expires=None,
        discard=True,
        comment=None,
        comment_url=None,
        rest={},
        rfc2109=False,
    )
    result = materialize_cookie(cookie)
    assert result["domain"] == ""
    assert result["name"] == "id"
    assert result["value"] == "123"
