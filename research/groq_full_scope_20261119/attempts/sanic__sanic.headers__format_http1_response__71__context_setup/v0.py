import pytest
from sanic.headers import format_http1_response, _HTTP1_STATUSLINES, STATUS_CODES

def test_format_http1_response_basic():
    """Normal case: status 200 with two headers."""
    headers = [(b"Content-Type", b"text/plain"), (b"Content-Length", b"5")]
    result = format_http1_response(200, headers)
    expected_start = b"HTTP/1.1 200 OK\r\n"
    assert result.startswith(expected_start)
    assert b"Content-Type: text/plain\r\n" in result
    assert b"Content-Length: 5\r\n" in result
    assert result.endswith(b"\r\n")

def test_format_http1_response_unknown_status():
    """Boundary case: status code not in STATUS_CODES should use UNKNOWN."""
    status = 999
    headers = [(b"X-Test", b"yes")]
    result = format_http1_response(status, headers)
    expected_start = _HTTP1_STATUSLINES[status]
    assert result.startswith(expected_start)
    assert b"X-Test: yes\r\n" in result
    assert result.endswith(b"\r\n")

def test_format_http1_response_invalid_header():
    """Error case: header values must be bytes; non-bytes raise TypeError."""
    headers = [(b"Valid", b"ok"), ("Invalid", b"oops")]  # first element is str
    with pytest.raises(TypeError):
        format_http1_response(200, headers)
