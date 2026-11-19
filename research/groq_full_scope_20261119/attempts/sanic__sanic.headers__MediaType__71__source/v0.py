import pytest
from sanic.headers import MediaType
from sanic.exceptions import InvalidHeader

def test_match_with_exact_and_parameters():
    """Exact match succeeds and parameters must match."""
    mt = MediaType("text", "html", charset="utf-8", q="0.8")
    # Exact string with same parameters
    assert mt.match("text/html; charset=utf-8; q=0.8") is mt
    # Same parameters but different order
    assert mt.match("text/html; q=0.8; charset=utf-8") is mt
    # Missing a parameter -> no match
    assert mt.match("text/html; charset=utf-8") is None
    # Different parameter value -> no match
    assert mt.match("text/html; charset=iso-8859-1; q=0.8") is None

def test_match_with_wildcards_and_q():
    """Wildcard matching works in both directions and q is ignored in match."""
    mt = MediaType("*", "*", q="0.5")
    # Wildcard matches any type/subtype
    assert mt.match("application/json") is mt
    assert mt.match("image/png") is mt
    # Wildcard subtype matches any subtype
    assert MediaType("text", "*").match("text/plain") is not None
    # Wildcard type matches any type
    assert MediaType("*", "html").match("application/html") is not None
    # Parameters must still match
    assert MediaType("text", "*", charset="utf-8").match("text/plain; charset=utf-8") is not None
    assert MediaType("text", "*", charset="utf-8").match("text/plain; charset=iso-8859-1") is None

def test_parse_invalid_and_missing_slash():
    """_parse returns None or raises ValueError for malformed inputs."""
    # No slash -> None
    assert MediaType._parse("plain") is None
    # Empty type or subtype -> ValueError
    with pytest.raises(ValueError, match="Invalid media type"):
        MediaType._parse("/html")
    with pytest.raises(ValueError, match="Invalid media type"):
        MediaType._parse("text/")
    # Leading/trailing spaces are stripped
    mt = MediaType._parse("  text / html ; charset = utf-8 ")
    assert isinstance(mt, MediaType)
    assert mt.type == "text"
    assert mt.subtype == "html"
    assert mt.params["charset"] == "utf-8"
