import pytest
from sanic.headers import AcceptList, MediaType, Matched
from sanic.exceptions import InvalidHeader

# Test 1: Basic matching with explicit types and q values
def test_acceptlist_match_basic():
    # Accept header: text/html;q=0.8, application/json;q=0.9, */*;q=0.5
    accept = AcceptList(
        MediaType("text/html", q=0.8),
        MediaType("application/json", q=0.9),
        MediaType("*/*", q=0.5)
    )
    # Query for application/json first, then text/html
    matched = accept.match("application/json", "text/html")
    # Should match application/json because higher q
    assert isinstance(matched, Matched)
    assert str(matched) == "application/json"
    assert matched.m == accept[1]  # second element

# Test 2: Wildcard matching and preference order
def test_acceptlist_match_wildcard_and_order():
    # Accept header: text/*;q=0.7, application/*;q=0.8, */*;q=0.6
    accept = AcceptList(
        MediaType("text/*", q=0.7),
        MediaType("application/*", q=0.8),
        MediaType("*/*", q=0.6)
    )
    # Query for image/png (no explicit match) and application/xml
    matched = accept.match("image/png", "application/xml")
    # Should match application/* because higher q than text/*
    assert str(matched) == "application/xml"
    assert matched.m == accept[1]  # application/* entry

# Test 3: No match when accept_wildcards is False
def test_acceptlist_no_match_without_wildcards():
    # Accept header: text/html;q=0.8, application/json;q=0.9
    accept = AcceptList(
        MediaType("text/html", q=0.8),
        MediaType("application/json", q=0.9)
    )
    # Query for image/png which is not present and no wildcard
    matched = accept.match("image/png", accept_wildcards=False)
    # Should return empty match
    assert str(matched) == ""
    assert matched.m is None
