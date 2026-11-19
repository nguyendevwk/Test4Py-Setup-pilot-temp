import pytest
from requests.cookies import RequestsCookieJar, Cookie
from httpie.sessions import materialize_cookies

def test_empty_jar_returns_empty_list():
    jar = RequestsCookieJar()
    result = materialize_cookies(jar)
    assert isinstance(result, list)
    assert result == []

def test_single_cookie_materializes_correctly():
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
        expires=None,
        discard=True,
        comment=None,
        comment_url=None,
        rest={}
    )
    jar.set_cookie(cookie)
    result = materialize_cookies(jar)
    assert len(result) == 1
    materialized = result[0]
    assert materialized["name"] == "sessionid"
    assert materialized["value"] == "abc123"
    assert materialized["domain"] == "example.com"
    assert materialized["path"] == "/"

def test_multiple_cookies_preserve_all_and_attributes():
    jar = RequestsCookieJar()
    jar.set("a", "1", domain="foo.com", path="/foo")
    jar.set("b", "2", domain="bar.com", path="/bar")
    jar.set("c", "3", domain="baz.com", path="/baz")
    result = materialize_cookies(jar)
    names = {c["name"] for c in result}
    assert names == {"a", "b", "c"}
    for c in result:
        assert "value" in c
        assert "domain" in c
        assert "path" in c
        assert c["value"] == str(c["value"])
