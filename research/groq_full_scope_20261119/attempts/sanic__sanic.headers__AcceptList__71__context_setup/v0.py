import pytest
from sanic.headers import AcceptList, Matched

# Helper to create a simple AcceptList with known media types
def make_accept_list(*mimes: str):
    # Each mime string is parsed into a MediaType by AcceptList constructor
    return AcceptList(*mimes)

def test_match_prefers_q_and_specificity():
    # Accept header with two entries: one with higher q, one more specific
    accept = make_accept_list("text/*;q=0.8", "text/html;q=0.5")
    # Search for text/html and application/json
    result = accept.match("text/html", "application/json")
    # Should match text/html because it is explicitly listed and has higher q
    assert isinstance(result, Matched)
    assert result.mime == "text/html"
    assert result.header is not None
    # The matched header should be the one from the AcceptList
    assert result.header.type == "text" and result.header.subtype == "html"

def test_match_with_wildcards_and_order():
    # Accept header with wildcard and specific type
    accept = make_accept_list("image/*;q=0.7", "image/png;q=0.9")
    # Search for image/png first, then image/jpeg
    result = accept.match("image/png", "image/jpeg")
    # Should match image/png because it appears earlier in the arguments
    assert result.mime == "image/png"
    # Now search with reverse order
    result2 = accept.match("image/jpeg", "image/png")
    # Should still match image/png because it has higher q
    assert result2.mime == "image/png"

def test_match_no_match_and_wildcard_disabled():
    # Accept header with only a wildcard
    accept = make_accept_list("*/*;q=0.5")
    # Search for a type not present
    result = accept.match("application/xml")
    # Should match because wildcard is present
    assert result.mime == "application/xml"
    # Disable wildcard matching
    result_no_wildcard = accept.match("application/xml", accept_wildcards=False)
    # Should be falsy because no explicit match
    assert not result_no_wildcard
    assert result_no_wildcard.mime == ""
    assert result_no_wildcard.header is None
