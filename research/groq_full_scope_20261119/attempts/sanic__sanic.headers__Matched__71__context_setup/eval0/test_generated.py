import pytest
from sanic.headers import Matched

# Helper: create a Matched instance from a MIME string
def mk(mime: str) -> Matched:
    return Matched.parse(mime)

def test_equality_same_mime_and_header():
    """Two Matched objects with identical MIME strings should compare equal."""
    a = mk("text/plain")
    b = mk("text/plain")
    assert a == b
    # Equality should be symmetric
    assert b == a
    # The bool value should be True because header is present
    assert bool(a)

def test_match_with_wildcard_subtype():
    """A MIME string with a wildcard subtype should match a concrete subtype."""
    a = mk("text/*")
    b = mk("text/html")
    # match returns the other Matched instance if compatible
    assert a.match(b) is b
    # The reverse match should also succeed
    assert b.match(a) is a
    # A non-matching type should return None
    c = mk("application/json")
    assert a.match(c) is None

def test_equality_with_different_headers():
    """Two Matched objects with different headers should not compare equal."""
    a = mk("image/png")
    b = mk("image/jpeg")
    assert a != b
    # Even though MIME strings differ, the comparison should be False
    assert not (a == b)
    # Comparing with a non-Matched type should return False
    assert a != "image/png"
