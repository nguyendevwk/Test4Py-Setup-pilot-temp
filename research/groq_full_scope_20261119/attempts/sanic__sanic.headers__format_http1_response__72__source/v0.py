import pytest
from sanic.headers import format_http1_response
from sanic.helpers import STATUS_CODES

def test_basic_response_formatting():
    """Verify that a typical 200 OK response with two headers is formatted correctly."""
    status = 200
    headers = [(b"Content-Type", b"text/plain"), (b"X-Custom", b"123")]
    result = format_http1_response(status, headers)
    expected = (
        STATUS_CODES[status] + b"\r\n"
        b"Content-Type: text/plain\r\n"
        b"X-Custom: 123\r\n"
        b"\r\n"
    )
    assert result == expected
    # Ensure the result is bytes and contains the CRLF terminator
    assert isinstance(result, bytes)
    assert result.endswith(b"\r\n\r\n")

def test_empty_headers_and_nonstandard_status():
    """Check that the function handles an empty header list and a non‑standard status code."""
    status = 418  # I'm a teapot
    headers = []
    result = format_http1_response(status, headers)
    expected = STATUS_CODES[status] + b"\r\n\r\n"
    assert result == expected
    # The status line should be present and no header lines should appear
    assert b"\r\n\r\n" in result
    assert b"\r\n\r\n\r\n" not in result

def test_invalid_header_tuple_raises_type_error():
    """Passing a header that is not a two‑item bytes tuple should raise a TypeError."""
    status = 200
    # Header with wrong type (string instead of bytes) and wrong length
    headers = [(b"Content-Type", "text/html"), ("Invalid", b"header")]
    with pytest.raises(TypeError):
        format_http1_response(status, headers)
