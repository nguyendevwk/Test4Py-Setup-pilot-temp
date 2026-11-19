import pytest
from sanic.headers import MediaType
from sanic.exceptions import InvalidHeader

def test_match_with_parameters_and_wildcards():
    # Base media type with a parameter and a wildcard subtype
    base = MediaType("application", "*", q="0.8", charset="utf-8")
    # Candidate with matching type, specific subtype, same parameter
    candidate = MediaType("application", "json", charset="utf-8")
    # Should match because subtype wildcard in base matches any subtype
    assert base.match(candidate) is base
    # Candidate with different parameter should not match
    candidate_diff = MediaType("application", "json", charset="iso-8859-1")
    assert base.match(candidate_diff) is None
    # Candidate with different type should not match
    candidate_type = MediaType("text", "html")
    assert base.match(candidate_type) is None

def test_has_wildcard_and_equality():
    # Media type with wildcard in type
    mt_wild = MediaType("*", "json")
    assert mt_wild.has_wildcard is True
    # Media type without wildcard
    mt_exact = MediaType("application", "json")
    assert mt_exact.has_wildcard is False
    # Equality ignores parameters
    mt1 = MediaType("application", "json", q="0.5")
    mt2 = MediaType("application", "json", q="1.0")
    assert mt1 == mt2
    # Equality with string without parameters
    assert mt1 == "application/json"
    # Equality with string containing parameters should raise ValueError
    with pytest.raises(ValueError):
        _ = mt1 == "application/json; q=0.5"

def test_parse_invalid_and_missing_slash():
    # Missing slash should return None
    assert MediaType._parse("applicationjson") is None
    # Empty type or subtype should raise ValueError
    with pytest.raises(ValueError):
        MediaType._parse("/json")
    with pytest.raises(ValueError):
        MediaType._parse("application/")
    # Invalid parameter format should raise ValueError
    with pytest.raises(ValueError):
        MediaType._parse("application/json;invalidparam")
