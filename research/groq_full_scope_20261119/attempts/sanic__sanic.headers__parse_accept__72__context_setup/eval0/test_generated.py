import pytest
from sanic.headers import parse_accept, AcceptList, InvalidHeader


def test_parse_accept_normal_and_ordering():
    # Accept header with multiple media types and q values
    header = "text/html;q=0.8, application/json, image/png;q=0.5, */*;q=0.1"
    result = parse_accept(header)
    # The result should be an AcceptList sorted by q and specificity
    assert isinstance(result, AcceptList)
    # The most preferred should be application/json (q=1.0, most specific)
    assert str(result[0]) == "application/json"
    # Next should be text/html with q=0.8
    assert str(result[1]) == "text/html;q=0.8"
    # Then image/png with q=0.5
    assert str(result[2]) == "image/png;q=0.5"
    # Finally */* with q=0.1
    assert str(result[3]) == "*/*;q=0.1"
    # The list should preserve the order of equal q values by specificity
    assert len(result) == 4


def test_parse_accept_empty_and_default_behavior():
    # Empty string should return an empty AcceptList (accept nothing)
    empty_result = parse_accept("")
    assert isinstance(empty_result, AcceptList)
    assert len(empty_result) == 0

    # None should default to "*/*" meaning all types accepted
    default_result = parse_accept(None)
    assert isinstance(default_result, AcceptList)
    assert len(default_result) == 1
    assert str(default_result[0]) == "*/*"


def test_parse_accept_invalid_header_raises():
    # Header with an invalid media type should raise InvalidHeader
    with pytest.raises(InvalidHeader) as excinfo:
        parse_accept("invalid/media;type")
    assert "Invalid header value in Accept" in str(excinfo.value)

    # Header with only commas should also raise
    with pytest.raises(InvalidHeader):
        parse_accept(",,,")

    # Header with a malformed q value should raise
    with pytest.raises(InvalidHeader):
        parse_accept("text/html;q=bad")
