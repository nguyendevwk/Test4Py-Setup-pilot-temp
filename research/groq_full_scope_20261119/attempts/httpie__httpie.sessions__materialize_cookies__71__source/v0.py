import pytest
from http.cookies import SimpleCookie
from http.cookiejar import Cookie
from requests.cookies import RequestsCookieJar

from httpie.sessions import materialize_cookies


def test_materialize_cookies_with_single_cookie():
    """Ensure a single cookie is correctly materialized into a dict."""
    jar = RequestsCookieJar()
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
        expires=1700000000,
        discard=False,
        comment=None,
        comment_url=None,
        rest={"HttpOnly": None},
        rfc2109=False,
    )
    jar.set_cookie(cookie)

    result = materialize_cookies(jar)

    assert isinstance(result, list)
    assert len(result) == 1
    cookie_dict = result[0]
    assert cookie_dict["name"] == "sessionid"
    assert cookie_dict["value"] == "abc123"
    assert cookie_dict["domain"] == "example.com"
    assert cookie_dict["path"] == "/"
    assert cookie_dict["expires"] == 1700000000
    assert cookie_dict["secure"] is False
    assert cookie_dict["httpOnly"] is True  # HttpOnly flag present


def test_materialize_cookies_with_multiple_cookies_and_order():
    """Check that multiple cookies are materialized and order is preserved."""
    jar = RequestsCookieJar()
    # Add two cookies with different domains
    jar.set_cookie(
        Cookie(
            version=0,
            name="a",
            value="1",
            port=None,
            port_specified=False,
            domain="a.com",
            domain_specified=True,
            domain_initial_dot=False,
            path="/",
            path_specified=True,
            secure=False,
            expires=None,
            discard=False,
            comment=None,
            comment_url=None,
            rest={},
            rfc2109=False,
        )
    )
    jar.set_cookie(
        Cookie(
            version=0,
            name="b",
            value="2",
            port=None,
            port_specified=False,
            domain="b.com",
            domain_specified=True,
            domain_initial_dot=False,
            path="/",
            path_specified=True,
            secure=True,
            expires=None,
            discard=False,
            comment=None,
            comment_url=None,
            rest={},
            rfc2109=False,
        )
    )

    result = materialize_cookies(jar)

    assert len(result) == 2
    # Order should match insertion order
    assert result[0]["name"] == "a"
    assert result[1]["name"] == "b"
    # Verify secure flag for second cookie
    assert result[1]["secure"] is True
    # First cookie should not be secure
    assert result[0]["secure"] is False


def test_materialize_cookies_with_invalid_input_raises_type_error():
    """Passing a non-RequestsCookieJar should raise a TypeError."""
    with pytest.raises(TypeError):
        materialize_cookies(None)
