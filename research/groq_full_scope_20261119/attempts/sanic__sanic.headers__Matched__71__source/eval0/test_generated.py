import pytest
from sanic.headers import Matched

def test_matched_equality_and_bool():
    """Test that Matched objects compare correctly and evaluate truthiness."""
    m1 = Matched.parse("text/plain")
    m2 = Matched.parse("text/plain")
    m3 = Matched.parse("text/html")

    # Equality should be True for identical MIME strings
    assert m1 == m2
    # Different MIME strings should not be equal
    assert m1 != m3
    # Truthiness depends on header presence
    assert bool(m1) is True
    assert bool(Matched("invalid", None)) is False

def test_matched_match_success_and_failure():
    """Test the match method for both successful and unsuccessful matches."""
    m1 = Matched.parse("application/json")
    m2 = Matched.parse("application/*")
    m3 = Matched.parse("text/*")

    # m1 matches m2 because subtype wildcard
    assert m1.match(m2) is m2
    # m1 does not match m3 because type differs
    assert m1.match(m3) is None
    # Matching with a string directly
    assert m1.match("application/*") is m2

def test_matched_parse_invalid_and_repr():
    """Test parsing of invalid MIME strings and representation."""
    # Parsing an invalid MIME string should produce a Matched with no header
    invalid = Matched.parse("not-a-mime")
    assert invalid.header is None
    # __repr__ should reflect no match
    assert repr(invalid) == "<no match>"
    # __str__ should return the raw string
    assert str(invalid) == "not-a-mime"
