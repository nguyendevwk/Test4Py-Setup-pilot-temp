import pytest
from http.cookies import SimpleCookie
from http.cookiejar import Cookie, CookieJar
from requests.cookies import RequestsCookieJar
from httpie.sessions import materialize_cookies


def test_materialize_cookies_empty_jar():
    """materialize_cookies should return an empty list for an empty jar."""
    jar = RequestsCookieJar()
    result = materialize_cookies(jar)
    assert isinstance(result, list)
    assert result == []


def test_materialize_cookies_single_cookie():
    """materialize_cookies should correctly serialize a single cookie."""
    jar = RequestsCookieJar()
    # Create a cookie with various attributes
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
    assert len(result) == 1
    serialized = result[0]
    # Basic attributes
    assert serialized["name"] == "sessionid"
    assert serialized["value"] == "abc123"
    assert serialized["domain"] == "example.com"
    assert serialized["path"] == "/"
    # Optional attributes
    assert serialized["expires"] == 1700000000
    assert serialized["secure"] is False
    assert serialized["httpOnly"] is True
    # Ensure no unexpected keys
    expected_keys = {
        "name", "value", "domain", "path", "expires",
        "secure", "httpOnly", "sameSite", "maxAge", "domainInitialDot",
        "port", "portSpecified", "pathSpecified", "discard", "comment",
        "commentUrl", "rfc2109", "rest",
    }
    assert set(serialized.keys()).issubset(expected_keys)


def test_materialize_cookies_multiple_cookies():
    """materialize_cookies should preserve order and serialize all cookies."""
    jar = RequestsCookieJar()
    # Add multiple cookies
    for i in range(3):
        cookie = Cookie(
            version=0,
            name=f"cookie{i}",
            value=f"value{i}",
            domain="example.com",
            path="/",
            secure=bool(i % 2),
            rest={"HttpOnly": None} if i % 2 == 0 else {},
        )
        jar.set_cookie(cookie)

    result = materialize_cookies(jar)
    assert len(result) == 3
    # Order should match insertion order
    for idx, entry in enumerate(result):
        assert entry["name"] == f"cookie{idx}"
        assert entry["value"] == f"value{idx}"
        # HttpOnly flag only for even indices
        assert entry["httpOnly"] == (idx % 2 == 0)
