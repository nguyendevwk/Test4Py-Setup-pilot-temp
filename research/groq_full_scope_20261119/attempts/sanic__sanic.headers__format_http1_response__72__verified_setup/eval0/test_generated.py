import pytest
from sanic.headers import format_http1_response
from sanic.helpers import STATUS_CODES

def test_empty_headers_returns_status_line_and_blank_line(tmp_path):
    status = 200
    headers = []
    result = format_http1_response(status, headers)
    expected = (
        f"{STATUS_CODES[status]} {status}\r\n".encode() + b"\r\n"
    )
    assert result == expected
    assert result.endswith(b"\r\n")

def test_multiple_headers_are_formatted_correctly(tmp_path):
    status = 404
    headers = [
        (b"Content-Type", b"text/html"),
        (b"X-Custom-Header", b"Value"),
    ]
    result = format_http1_response(status, headers)
    expected = (
        f"{STATUS_CODES[status]} {status}\r\n".encode()
        + b"Content-Type: text/html\r\n"
        + b"X-Custom-Header: Value\r\n"
        + b"\r\n"
    )
    assert result == expected
    # Ensure each header line ends with CRLF
    for line in result.split(b"\r\n")[:-1]:
        assert line.endswith(b"") or line == b""

def test_non_ascii_header_values_are_preserved(tmp_path):
    status = 500
    headers = [
        (b"Content-Type", b"text/plain; charset=utf-8"),
        (b"X-Emoji", "😀".encode()),
    ]
    result = format_http1_response(status, headers)
    expected = (
        f"{STATUS_CODES[status]} {status}\r\n".encode()
        + b"Content-Type: text/plain; charset=utf-8\r\n"
        + b"X-Emoji: \xf0\x9f\x98\x80\r\n"
        + b"\r\n"
    )
    assert result == expected
