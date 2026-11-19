import pytest
from sanic.headers import Matched

def test_parse_and_basic_properties(tmp_path):
    """Test that parsing a MIME string creates a Matched with expected attributes."""
    m = Matched.parse("text/plain")
    # The raw MIME string should be preserved
    assert str(m) == "text/plain"
    # The header should be a MediaType instance (truthy)
    assert m.header is not None
    # Boolean context should be True when header is present
    assert bool(m) is True
    # Representation should include the matched header
    rep = repr(m)
    assert "<text/plain matched" in rep
    assert ">" in rep

def test_equality_and_comparison(tmp_path):
    """Test equality between Matched objects and between Matched and raw MIME strings."""
    m1 = Matched.parse("application/json")
    m2 = Matched.parse("application/json")
    # Two Matched objects with the same MIME should be equal
    assert m1 == m2
    # Equality with a raw string should also succeed
    assert m1 == "application/json"
    # Equality with a different MIME should fail
    assert m1 != "text/html"
    # Equality with an unrelated type should return False
    assert m1 != 42

def test_match_with_missing_header(tmp_path):
    """Test that match returns None when either side has no header."""
    # Create a Matched with no header by manually passing None
    m_no_header = Matched("image/png", None)
    # Matching against any string should return None
    assert m_no_header.match("image/png") is None
    # Matching against another Matched with no header should also return None
    other_no_header = Matched("image/png", None)
    assert m_no_header.match(other_no_header) is None
