import pytest
from sanic.headers import format_http1_response, _HTTP1_STATUSLINES, STATUS_CODES

def test_format_http1_response_with_headers():
    # Normal case: status 200 with two headers
    headers = [
        (b"Content-Type", b"text/plain"),
        (b"Content-Length", b"13"),
    ]
    result = format_http1_response(200, headers)
    # Expected status line
    assert result.startswith(b"HTTP/1.1 200 OK\r\n")
    # Each header line should be present
    assert b"Content-Type: text/plain\r\n" in result
    assert b"Content-Length: 13\r\n" in result
    # The header block should end with an empty line
    assert result.endswith(b"\r\n\r\n")

def test_format_http1_response_no_headers():
    # Boundary case: status 404 with no headers
    result = format_http1_response(404, [])
    # Status line should use the correct reason phrase
    assert result.startswith(b"HTTP/1.1 404 Not Found\r\n")
    # No header lines should be present except the terminating CRLF
    assert result == b"HTTP/1.1 404 Not Found\r\n\r\n"

def test_format_http1_response_invalid_status():
    # Error case: status code outside the precomputed range triggers IndexError
    with pytest.raises(IndexError):
        format_http1_response(1000, [])
