import pytest
from sanic.headers import Matched

def test_matched_equality_same_mime_and_header():
    """Two Matched objects with identical MIME strings and headers should compare equal."""
    m1 = Matched.parse("text/plain; charset=utf-8")
    m2 = Matched.parse("text/plain; charset=utf-8")
    # They are distinct objects but represent the same header
    assert m1 == m2
    # Equality should be symmetric
    assert m2 == m1
    # The bool value should be True because headers are present
    assert bool(m1) is True
    assert bool(m2) is True

def test_matched_match_wildcard_subtype():
    """A MIME string with a wildcard subtype should match a concrete subtype."""
    # Header with wildcard subtype
    wildcard = Matched.parse("text/*")
    # Concrete header
    concrete = Matched.parse("text/html")
    # The wildcard should match the concrete type
    assert wildcard.match(concrete) == concrete
    # The reverse match should also succeed
    assert concrete.match(wildcard) == wildcard

def test_matched_equality_with_different_headers():
    """Two Matched objects with the same MIME string but different headers should not compare equal."""
    m1 = Matched.parse("application/json")
    # Create a second Matched with a different header by parsing a different string
    m2 = Matched.parse("application/xml")
    # Even though the MIME strings differ, the objects should not be equal
    assert m1 != m2
    # Ensure that the bool values reflect the presence of headers
    assert bool(m1) is True
    assert bool(m2) is True
