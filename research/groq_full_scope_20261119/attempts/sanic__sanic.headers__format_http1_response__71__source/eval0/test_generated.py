import pytest
from sanic.headers import format_http1_response
from sanic.exceptions import InvalidHeader

# Test 1: Normal response with multiple headers
def test_format_http1_response_with_headers():
    status = 200
    headers = [
        (b"Content-Type", b"text/plain"),
        (b"Content-Length", b"13"),
    ]
    result = format_http1_response(status, headers)
    expected = (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: text/plain\r\n"
        b"Content-Length: 13\r\n"
        b"\r\n"
    )
    assert result == expected

# Test 2: Response with no headers (boundary case)
def test_format_http1_response_no_headers():
    status = 404
    headers = []
    result = format_http1_response(status, headers)
    expected = (
        b"HTTP/1.1 404 Not Found\r\n"
        b"\r\n"
    )
    assert result == expected

# Test 3: Invalid status code raises KeyError
def test_format_http1_response_invalid_status():
    status = 999  # not a standard status code
    headers = [(b"X-Test", b"value")]
    with pytest.raises(KeyError):
        format_http1_response(status, headers)
