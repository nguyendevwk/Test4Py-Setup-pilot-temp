import pytest
from sanic.headers import Matched, MediaType
from sanic.exceptions import InvalidHeader

def test_matched_equality_and_bool(tmp_path):
    # Create two Matched objects with identical MIME strings and headers
    m1 = Matched.parse("text/plain; charset=utf-8")
    m2 = Matched.parse("text/plain; charset=utf-8")
    # They should be equal and truthy
    assert m1 == m2
    assert bool(m1) is True
    # Changing the MIME string should break equality
    m3 = Matched.parse("text/html; charset=utf-8")
    assert m1 != m3
    # A Matched with no header is falsy
    m_no_header = Matched("application/json", None)
    assert bool(m_no_header) is False
    # Representation includes header when present
    assert "<text/plain; charset=utf-8> matched" in repr(m1)
    # Representation for no match
    assert repr(m_no_header) == "<no match>"

def test_matched_match_wildcards(tmp_path):
    # Header with wildcard subtype
    header_wild = Matched.parse("text/*")
    # Header with specific subtype
    header_specific = Matched.parse("text/plain")
    # They should match each other
    assert header_wild.match(header_specific) == header_specific
    assert header_specific.match(header_wild) == header_wild
    # Header with wildcard type
    header_type_wild = Matched.parse("*/*")
    # Should match any header
    assert header_type_wild.match(header_specific) == header_specific
    assert header_specific.match(header_type_wild) == header_type_wild
    # Non-matching types
    header_other = Matched.parse("image/png")
    assert header_specific.match(header_other) is None
    assert header_other.match(header_specific) is None

def test_matched_parse_invalid_header(tmp_path):
    # Invalid MIME string should raise InvalidHeader during parsing
    with pytest.raises(InvalidHeader):
        Matched.parse("invalid/mime; charset")
    # Valid MIME string but with unsupported parameters should still parse
    m = Matched.parse("application/json; q=0.9")
    assert isinstance(m.header, MediaType)
    assert m.header.type == "application"
    assert m.header.subtype == "json"
    # The parsed header should preserve parameters
    assert m.header.params.get("q") == "0.9"
