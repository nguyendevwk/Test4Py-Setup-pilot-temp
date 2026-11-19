import pytest
from sanic.headers import AcceptList

# Minimal stand‑in for the MediaType class used by AcceptList.
class DummyMediaType:
    def __init__(self, mime: str, q: float = 1.0):
        self.mime = mime
        self.q = q
        self.has_wildcard = "*" in mime

    def match(self, other: str) -> bool:
        # Simple wildcard matching: '*' matches anything in that position
        t1, t2 = self.mime.split("/", 1)
        o1, o2 = other.split("/", 1)
        return (t1 == "*" or t1 == o1) and (t2 == "*" or t2 == o2)

    def __str__(self):
        return f"{self.mime};q={self.q}"


def test_match_prefers_higher_q_and_specificity():
    """AcceptList should pick the entry with the highest q and most specific type."""
    al = AcceptList(
        DummyMediaType("text/html", q=0.8),
        DummyMediaType("text/*", q=0.9),
        DummyMediaType("application/json", q=0.7),
    )
    matched = al.match("application/json", "text/html")
    # The best match is text/* because it has higher q than text/html
    assert matched.m.mime == "text/*"
    assert matched.m.q == 0.9
    # The returned string should be the mime argument that matched
    assert str(matched) == "text/html"


def test_match_returns_empty_when_no_match():
    """When no Accept header entry matches, match() returns an empty Matched."""
    al = AcceptList(
        DummyMediaType("application/xml", q=0.5),
        DummyMediaType("image/png", q=0.6),
    )
    matched = al.match("text/plain")
    assert matched.m is None
    assert matched.mime == ""  # falsy string
    assert not matched  # Matched is falsy when no match


def test_wildcard_handling_and_argument_order():
    """Wildcard entries should match any mime, and argument order influences tie‑break."""
    al = AcceptList(
        DummyMediaType("*/*", q=0.1),
        DummyMediaType("text/*", q=0.5),
        DummyMediaType("text/html", q=0.5),
    )
    # Both text/html and text/* have same q; argument order decides
    matched = al.match("text/html", "text/plain")
    # text/html is first argument, so it should win over text/plain
    assert matched.m.mime == "text/html"
    assert matched.m.q == 0.5
    # If we reverse the argument order, text/plain should win
    matched_rev = al.match("text/plain", "text/html")
    assert matched_rev.m.mime == "text/plain"
    assert matched_rev.m.q == 0.5
