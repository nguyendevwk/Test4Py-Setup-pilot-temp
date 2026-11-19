import pytest
from sanic.headers import AcceptList, MediaType, Matched
from sanic.exceptions import InvalidHeader

def test_accept_list_match_preference_and_q_values():
    # Construct AcceptList with varying q values and specificity
    accept = AcceptList(
        MediaType("text/html; q=0.8"),
        MediaType("application/json; q=0.9"),
        MediaType("image/*; q=0.7"),
        MediaType("*/*; q=0.5")
    )
    # The most preferred match should be application/json
    matched = accept.match("application/json", "text/html", "image/png")
    assert isinstance(matched, Matched)
    assert matched.mime == "application/json"
    assert matched.m.type == "application" and matched.m.subtype == "json"
    # The matched MediaType should be the one from the AcceptList
    assert matched.m is accept[1]

def test_accept_list_match_with_wildcards_and_order():
    # Accept header with wildcard and specific types
    accept = AcceptList(
        MediaType("text/*; q=0.6"),
        MediaType("text/html; q=0.8"),
        MediaType("*/*; q=0.4")
    )
    # When searching for text/html first, it should match the specific type
    matched = accept.match("text/html", "text/plain")
    assert matched.mime == "text/html"
    # If we search for text/plain first, it should match the wildcard text/*
    matched2 = accept.match("text/plain", "text/html")
    assert matched2.mime == "text/plain"
    # If we disable wildcard matching, only explicit matches should be considered
    matched3 = accept.match("image/png", accept_wildcards=False)
    assert matched3.mime == "" and matched3.m is None

def test_accept_list_str_representation_and_invalid_header():
    # AcceptList should format as a comma-separated string
    accept = AcceptList(
        MediaType("application/xml; q=0.9"),
        MediaType("application/json; q=0.8")
    )
    assert str(accept) == "application/xml; q=0.9, application/json; q=0.8"

    # Creating a MediaType with an invalid MIME type should raise InvalidHeader
    with pytest.raises(InvalidHeader):
        MediaType("invalid/mime; q=1.0")
