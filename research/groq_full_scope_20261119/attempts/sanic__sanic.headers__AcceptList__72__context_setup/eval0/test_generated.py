import pytest
from sanic.headers import AcceptList, MediaType, Matched
from sanic.exceptions import InvalidHeader


def test_acceptlist_match_preference_and_q_values():
    """
    Verify that AcceptList.match respects q values, specificity, and argument order.
    """
    # Construct Accept header with varying q values and specificity
    accept_header = AcceptList(
        MediaType("text/html; q=0.8"),
        MediaType("application/json; q=0.9"),
        MediaType("image/*; q=0.7"),
        MediaType("*/*; q=0.5")
    )

    # The client prefers application/json over text/html due to higher q
    result = accept_header.match("text/html", "application/json")
    assert isinstance(result, Matched)
    assert result.mime == "application/json"
    assert result.header == accept_header[1]  # second entry

    # If we reverse the order of arguments, the first argument wins if q equal
    result = accept_header.match("image/png", "text/html")
    # image/png matches image/* (third entry) which has q=0.7
    # text/html has q=0.8 but is second argument, so image/png wins
    assert result.mime == "image/png"
    assert result.header == accept_header[2]

    # Wildcard matching should work when accept_wildcards is True
    result = accept_header.match("application/xml")
    assert result.mime == "application/xml"
    assert result.header == accept_header[3]  # */*


def test_acceptlist_match_no_match_returns_empty():
    """
    Verify that AcceptList.match returns an empty Matched when no match is found.
    """
    accept_header = AcceptList(
        MediaType("text/html; q=0.8"),
        MediaType("application/json; q=0.9")
    )

    # No Accept header entry matches the requested MIME type
    result = accept_header.match("image/png", accept_wildcards=False)
    assert isinstance(result, Matched)
    assert not result  # __bool__ should be False
    assert result.mime == ""
    assert result.header is None

    # Even with wildcards allowed, no match if header has no wildcard
    result = accept_header.match("image/png", accept_wildcards=True)
    assert isinstance(result, Matched)
    assert not result
    assert result.mime == ""
    assert result.header is None


def test_acceptlist_invalid_header_raises_exception():
    """
    Verify that constructing MediaType with an invalid header raises InvalidHeader.
    """
    with pytest.raises(InvalidHeader):
        # Invalid MIME type string should trigger parsing error
        MediaType("invalid/mime; q=abc")

    # Ensure that AcceptList can be constructed with valid entries only
    valid_header = AcceptList(MediaType("text/plain"))
    assert len(valid_header) == 1
    assert isinstance(valid_header[0], MediaType)
