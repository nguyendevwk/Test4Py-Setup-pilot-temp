import pytest
from sanic.headers import parse_accept, AcceptList, InvalidHeader, MediaType


def test_parse_accept_normal_and_ordering():
    # Accept header with multiple media types and q values
    header = "text/html;q=0.8, application/json, text/plain;q=0.5, */*;q=0.1"
    result = parse_accept(header)
    # The result should be an AcceptList sorted by q and specificity
    assert isinstance(result, AcceptList)
    # The most preferred should be application/json (q=1.0, most specific)
    assert str(result[0]) == "application/json"
    # Next should be text/html (q=0.8)
    assert str(result[1]) == "text/html;q=0.8"
    # Then text/plain (q=0.5)
    assert str(result[2]) == "text/plain;q=0.5"
    # Finally */* (q=0.1)
    assert str(result[3]) == "*/*;q=0.1"
    # Ensure the list can be matched correctly
    matched = result.match("application/json", "text/html")
    assert matched.mime == "application/json"
    assert matched.header == MediaType._parse("application/json")


def test_parse_accept_empty_and_missing():
    # Empty string should return an empty AcceptList (accept nothing)
    empty = parse_accept("")
    assert isinstance(empty, AcceptList)
    assert len(empty) == 0

    # None should default to "*/*" (accept everything)
    none_header = parse_accept(None)
    assert isinstance(none_header, AcceptList)
    assert len(none_header) == 1
    assert str(none_header[0]) == "*/*"


def test_parse_accept_invalid_header_raises():
    # Header with an invalid media type should raise InvalidHeader
    with pytest.raises(InvalidHeader) as excinfo:
        parse_accept("invalid/media; q=abc")
    assert "Invalid header value in Accept" in str(excinfo.value)

    # Header with only commas should also raise
    with pytest.raises(InvalidHeader):
        parse_accept(", , ,")
