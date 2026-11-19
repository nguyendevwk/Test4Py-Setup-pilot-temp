import pytest
from sanic.headers import parse_accept, AcceptList, MediaType
from sanic.exceptions import InvalidHeader

def test_parse_accept_normal_header():
    # Accept header with multiple media types and quality values
    header = "text/html, application/json;q=0.8, image/png;q=0.5, */*;q=0.1"
    result = parse_accept(header)
    # The result should be an AcceptList sorted by quality and type
    assert isinstance(result, AcceptList)
    # The first element should be the highest quality media type
    assert result[0].type == "text/html"
    # The second should be application/json with q=0.8
    assert result[1].type == "application/json"
    assert result[1].q == 0.8
    # The last should be */* with q=0.1
    assert result[-1].type == "*"
    assert result[-1].subtype == "*"
    assert result[-1].q == 0.1

def test_parse_accept_empty_and_missing_header():
    # Empty string should return an empty AcceptList (accept nothing)
    empty_result = parse_accept("")
    assert isinstance(empty_result, AcceptList)
    assert len(empty_result) == 0

    # None should default to "*/*" (accept everything)
    none_result = parse_accept(None)
    assert isinstance(none_result, AcceptList)
    assert len(none_result) == 1
    assert none_result[0].type == "*"
    assert none_result[0].subtype == "*"

def test_parse_accept_invalid_header_raises():
    # Header with an invalid media type should raise InvalidHeader
    invalid_header = "invalid/media; q=abc"
    with pytest.raises(InvalidHeader) as excinfo:
        parse_accept(invalid_header)
    assert "Invalid header value in Accept" in str(excinfo.value)
