import pytest
from sanic.headers import MediaType
from sanic.exceptions import InvalidHeader

def test_match_with_wildcards_and_parameters():
    # MediaType with wildcard subtype and a parameter
    mt = MediaType("text", "*", q="0.8")
    # Should match a concrete subtype with the same parameter
    assert mt.match("text/plain; q=0.8") is mt
    # Should not match if parameter differs
    assert mt.match("text/plain; q=0.5") is None
    # Should match if the other side has a wildcard subtype
    assert mt.match("text/*; q=0.8") is mt
    # Should not match if type differs
    assert mt.match("application/*; q=0.8") is None

def test_equality_and_repr():
    # Equality ignores parameters
    a = MediaType("image", "png", q="0.9")
    b = MediaType("image", "png", q="0.5")
    assert a == b
    # Equality with string ignores parameters
    assert a == "image/png"
    # Representation includes all parameters
    assert repr(a) == "image/png;q=0.9"
    # Comparing string with parameters raises ValueError
    with pytest.raises(ValueError):
        a == "image/png; q=0.9"

def test_parse_invalid_and_missing_parts():
    # Missing slash should return None
    assert MediaType._parse("textplain") is None
    # Empty type or subtype raises ValueError
    with pytest.raises(ValueError):
        MediaType._parse("/plain")
    with pytest.raises(ValueError):
        MediaType._parse("text/")
    # Correct parsing with parameters
    mt = MediaType._parse("application/json; charset=utf-8")
    assert isinstance(mt, MediaType)
    assert mt.type == "application"
    assert mt.subtype == "json"
    assert mt.params["charset"] == "utf-8"
