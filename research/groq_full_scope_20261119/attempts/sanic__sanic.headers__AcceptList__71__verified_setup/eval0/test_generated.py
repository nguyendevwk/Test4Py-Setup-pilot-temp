import pytest
from sanic.headers import AcceptList, Matched

# Minimal stand‑in for the MediaType class used by AcceptList.
# It implements only the attributes and methods required for the tests.
class DummyMediaType:
    def __init__(self, mime: str, q: float = 1.0):
        self.mime = mime
        self.q = q
        self.has_wildcard = "*" in mime

    def match(self, other: str) -> bool:
        # Very small matching logic: exact match or wildcard match
        if self.has_wildcard:
            return True
        return self.mime == other

    def __str__(self):
        return f"{self.mime};q={self.q}"


def test_acceptlist_match_prefers_higher_q_and_specificity():
    """AcceptList.match should return the most preferred media type."""
    # Two media types: one with higher q, one with wildcard
    mt_html = DummyMediaType("text/html", q=0.8)
    mt_any = DummyMediaType("*/*", q=1.0)
    al = AcceptList(mt_html, mt_any)

    # The client prefers text/html, which is present in the list
    matched = al.match("text/html")
    assert isinstance(matched, Matched)
    assert matched.mime == "text/html"
    assert matched.m is mt_html
    # The string representation should be the mime string
    assert str(matched) == "text/html"


def test_acceptlist_str_formats_header_value():
    """The string representation of AcceptList should be a comma separated list."""
    mt_json = DummyMediaType("application/json", q=0.9)
    mt_xml = DummyMediaType("application/xml", q=0.8)
    al = AcceptList(mt_json, mt_xml)

    header_value = str(al)
    # The order should be preserved
    assert header_value == "application/json;q=0.9, application/xml;q=0.8"


def test_acceptlist_match_no_match_returns_empty():
    """When no media type matches, match should return an empty Matched."""
    mt_html = DummyMediaType("text/html", q=0.8)
    al = AcceptList(mt_html)

    matched = al.match("application/json")
    assert isinstance(matched, Matched)
    # No match: mime string is empty and m is None
    assert matched.mime == ""
    assert matched.m is None
    assert not matched  # falsy when no match
