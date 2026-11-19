import pytest
from sanic.headers import MediaType
from sanic.exceptions import InvalidHeader

def test_match_with_parameters_and_wildcards():
    # MediaType with specific parameters
    mt = MediaType("application", "json", q="0.8", charset="utf-8")
    # Should match exact same type/subtype and parameters
    assert mt.match("application/json; charset=utf-8") is mt
    # Should not match if parameters differ
    assert mt.match("application/json; charset=iso-8859-1") is None
    # Wildcard subtype should match any subtype
    wildcard = MediaType("application", "*")
    assert wildcard.match("application/json") is wildcard
    # Wildcard type should match any type
    wildcard_type = MediaType("*", "json")
    assert wildcard_type.match("application/json") is wildcard_type
    # Both wildcards should match any
    both = MediaType("*", "*")
    assert both.match("text/plain") is both

def test_equality_and_repr():
    mt1 = MediaType("text", "html", charset="utf-8")
    mt2 = MediaType("text", "html")
    # Equality ignores parameters
    assert mt1 == mt2
    # Equality with string ignores parameters
    assert mt1 == "text/html"
    # String with parameters raises ValueError
    with pytest.raises(ValueError):
        mt1 == "text/html; charset=utf-8"
    # Representation includes parameters in insertion order
    assert repr(mt1) == "text/html;charset=utf-8"

def test_parse_invalid_and_missing_parts():
    # Missing slash
    assert MediaType._parse("applicationjson") is None
    # Empty type or subtype
    with pytest.raises(ValueError):
        MediaType._parse("/json")
    with pytest.raises(ValueError):
        MediaType._parse("application/")
    # Correct parsing with parameters
    parsed = MediaType._parse("image/png; resolution=high")
    assert isinstance(parsed, MediaType)
    assert parsed.type == "image"
    assert parsed.subtype == "png"
    assert parsed.params["resolution"] == "high"
