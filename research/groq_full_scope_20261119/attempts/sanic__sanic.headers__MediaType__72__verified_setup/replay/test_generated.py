import pytest
from sanic.headers import MediaType
from sanic.exceptions import InvalidHeader

def test_match_with_wildcards_and_parameters():
    # MediaType with wildcard subtype and a parameter
    mt = MediaType("application", "*", q="0.8", charset="utf-8")
    # Should match a concrete subtype with the same parameter
    assert mt.match("application/json; charset=utf-8") is mt
    # Should not match if parameter differs
    assert mt.match("application/json; charset=iso-8859-1") is None
    # Should match a wildcard subtype with no parameters
    assert mt.match("application/*") is mt
    # Should not match a different type
    assert mt.match("text/*") is None

def test_equality_and_repr():
    mt1 = MediaType("text", "html", charset="utf-8")
    mt2 = MediaType("text", "html", charset="utf-8")
    mt3 = MediaType("text", "html")
    # Equality ignores parameters
    assert mt1 == mt2
    assert mt1 == mt3
    # Equality with string ignores parameters
    assert mt1 == "text/html"
    # __repr__ includes parameters in order of insertion
    repr_str = repr(mt1)
    assert repr_str.startswith("text/html")
    assert ";charset=utf-8" in repr_str

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
        MediaType._parse("application/json; charset")
