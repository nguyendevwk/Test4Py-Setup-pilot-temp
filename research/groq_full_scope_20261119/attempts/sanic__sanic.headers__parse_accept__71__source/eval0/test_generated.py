import pytest
from sanic.headers import parse_accept, AcceptList, MediaType
from sanic.exceptions import InvalidHeader

def test_parse_accept_normal():
    # A typical Accept header with quality values and wildcards
    header = "text/html;q=0.8, application/json, */*;q=0.1"
    result = parse_accept(header)
    # The result should be an AcceptList sorted by preference
    assert isinstance(result, AcceptList)
    # The first item should be application/json (q=1.0 by default)
    assert result[0] == MediaType("application/json")
    # The second item should be text/html with q=0.8
    assert result[1] == MediaType("text/html", q=0.8)
    # The last item should be */* with q=0.1
    assert result[2] == MediaType("*/*", q=0.1)

def test_parse_accept_boundary_empty_and_none():
    # Empty string should return an empty AcceptList (accept nothing)
    empty_result = parse_accept("")
    assert isinstance(empty_result, AcceptList)
    assert len(empty_result) == 0

    # None should default to "*/*" (accept everything)
    none_result = parse_accept(None)
    assert isinstance(none_result, AcceptList)
    assert len(none_result) == 1
    assert none_result[0] == MediaType("*/*")

def test_parse_accept_error_invalid_header():
    # An invalid Accept header (e.g., malformed quality value) should raise InvalidHeader
    invalid_header = "text/html;q=invalid"
    with pytest.raises(InvalidHeader) as excinfo:
        parse_accept(invalid_header)
    assert "Invalid header value in Accept" in str(excinfo.value)
