import pytest
from sanic.headers import format_http1_response

def test_format_http1_response_with_headers():
    """Normal case: status 200 with two headers."""
    status = 200
    headers = [
        (b"Content-Type", b"text/plain"),
        (b"Content-Length", b"13"),
    ]
    result = format_http1_response(status, headers)
    # Expected status line from Sanic's internal mapping
    expected_status_line = b"HTTP/1.1 200 OK\r\n"
    # Expected header lines
    expected_headers = (
        b"Content-Type: text/plain\r\n"
        b"Content-Length: 13\r\n"
        b"\r\n"
    )
    assert result == expected_status_line + expected_headers

def test_format_http1_response_no_headers():
    """Boundary case: status 404 with no headers."""
    status = 404
    headers = []
    result = format_http1_response(status, headers)
    expected_status_line = b"HTTP/1.1 404 Not Found\r\n"
    expected = expected_status_line + b"\r\n"
    assert result == expected

def test_format_http1_response_invalid_status():
    """Error case: unknown status code raises KeyError."""
    status = 999  # not a standard HTTP status
    headers = [(b"X-Test", b"1")]
    with pytest.raises(KeyError):
        format_http1_response(status, headers)
