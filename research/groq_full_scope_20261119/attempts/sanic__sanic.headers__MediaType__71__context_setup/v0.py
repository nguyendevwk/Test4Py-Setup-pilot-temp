import pytest
from sanic.headers import MediaType
from sanic.exceptions import InvalidHeader

def test_match_with_wildcards_and_parameters():
    # MediaType with wildcard subtype and explicit type
    mt = MediaType("application", "*", q="0.8")
    # Should match any subtype of application
    assert mt.match("application/json") is mt
    # Should match with parameters if they match
    assert mt.match("application/json; charset=utf-8") is mt
    # Should not match if parameters differ
    assert mt.match("application/json; charset=iso-8859-1") is None
    # Should match when other side has wildcard subtype
    assert mt.match(MediaType("application", "*", q="0.5")) is mt
    # Should not match when type differs
    assert mt.match("text/html") is None

def test_equality_and_repr():
    mt1 = MediaType("text", "plain", charset="utf-8")
    mt2 = MediaType("text", "plain", charset="utf-8")
    mt3 = MediaType("text", "plain")
    # Equality ignores parameters
    assert mt1 == mt2
    assert mt1 == mt3
    # Equality with string ignores parameters
    assert mt1 == "text/plain"
    # __repr__ includes parameters
    assert repr(mt1) == "text/plain;charset=utf-8"
    # Equality with string containing parameters raises ValueError
    with pytest.raises(ValueError):
        _ = mt1 == "text/plain; charset=utf-8"

def test_parse_invalid_and_missing_parts():
    # Missing slash should return None
    assert MediaType._parse("applicationjson") is None
    # Empty type or subtype raises ValueError
    with pytest.raises(ValueError):
        MediaType._parse("/json")
    with pytest.raises(ValueError):
        MediaType._parse("application/")
    # Parameters without '=' should raise ValueError
    with pytest.raises(ValueError):
        MediaType._parse("application/json; charset")
