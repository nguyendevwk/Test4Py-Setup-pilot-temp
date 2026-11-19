import pytest
from sanic.headers import Matched

# Test 1: Parsing a simple MIME string creates a Matched with a non‑None header
def test_parse_simple_mime(tmp_path):
    m = Matched.parse("text/plain")
    # The parsed MIME string should be preserved
    assert str(m) == "text/plain"
    # The header should be a MediaType instance (truthy)
    assert m.header is not None
    # The object should evaluate to True
    assert bool(m) is True

# Test 2: Matching two compatible MIME strings returns the matched object
def test_match_compatible_mime():
    m1 = Matched.parse("application/json")
    m2 = Matched.parse("application/json")
    # match should return the other Matched instance when compatible
    result = m1.match(m2)
    assert result is m2
    # The match should also work when the other is a string
    result_str = m1.match("application/json")
    assert isinstance(result_str, Matched)
    assert result_str.mime == "application/json"

# Test 3: Comparing with an unsupported type yields False and does not raise
def test_equality_with_unsupported_type():
    m = Matched.parse("image/png")
    # Comparing with an integer should return False, not raise
    assert (m == 42) is False
    # Comparing with a list should also return False
    assert (m == ["image", "png"]) is False
    # Comparing with a string that is not a valid MIME should return False
    assert (m == "not/a/mime") is False
