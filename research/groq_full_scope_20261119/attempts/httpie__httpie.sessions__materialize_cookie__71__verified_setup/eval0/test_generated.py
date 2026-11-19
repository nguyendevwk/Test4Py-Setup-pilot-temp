import pytest
from http.cookiejar import Cookie
from httpie.sessions import materialize_cookie

# Helper to create a Cookie with minimal required arguments
def make_cookie(
    name: str,
    value: str,
    domain: str = "",
    path: str = "/",
    rest: dict | None = None,
    **kwargs,
) -> Cookie:
    return Cookie(
        version=0,
        name=name,
        value=value,
        port=None,
        port_specified=False,
        domain=domain,
        domain_specified=bool(domain),
        domain_initial_dot=domain.startswith("."),
        path=path,
        path_specified=True,
        secure=False,
        expires=None,
        discard=True,
        comment=None,
        comment_url=None,
        rest=rest or {},
        rfc2109=False,
        **kwargs,
    )

def test_materialize_cookie_preserves_attributes():
    """materialize_cookie should return a dict with all kept options."""
    cookie = make_cookie(name="foo", value="bar", domain="example.com", path="/")
    result = materialize_cookie(cookie)
    # The result should contain the cookie's name, value, domain, path, etc.
    assert result["name"] == "foo"
    assert result["value"] == "bar"
    assert result["domain"] == "example.com"
    assert result["path"] == "/"
    # Ensure that the result is a plain dict and not a Cookie instance
    assert isinstance(result, dict)

def test_materialize_cookie_explicit_none_domain():
    """If rest contains 'is_explicit_none' and domain is empty, domain becomes None."""
    cookie = make_cookie(
        name="baz",
        value="qux",
        domain="",
        rest={"is_explicit_none": True},
    )
    result = materialize_cookie(cookie)
    assert result["domain"] is None

def test_materialize_cookie_no_explicit_none_domain():
    """If rest does not contain 'is_explicit_none', domain remains unchanged."""
    cookie = make_cookie(
        name="alpha",
        value="beta",
        domain="",
        rest={},  # no explicit_none flag
    )
    result = materialize_cookie(cookie)
    assert result["domain"] == ""
