import pytest
from httpie.output.formatters.headers import HeadersFormatter


def test_sorting_of_headers():
    """Headers should be sorted alphabetically by name."""
    formatter = HeadersFormatter(format_options={"headers": {"sort": True}})
    raw = (
        "HTTP/1.1 200 OK\r\n"
        "z-Header: last\r\n"
        "a-Header: first\r\n"
        "m-Header: middle\r\n"
    )
    expected = (
        "HTTP/1.1 200 OK\r\n"
        "a-Header: first\r\n"
        "m-Header: middle\r\n"
        "z-Header: last\r\n"
    )
    assert formatter.format_headers(raw) == expected


def test_order_of_same_name_headers_preserved():
    """Headers with the same name should keep their relative order."""
    formatter = HeadersFormatter(format_options={"headers": {"sort": True}})
    raw = (
        "HTTP/1.1 200 OK\r\n"
        "Set-Cookie: a=1\r\n"
        "Set-Cookie: b=2\r\n"
        "Set-Cookie: c=3\r\n"
        "Content-Type: text/plain\r\n"
    )
    expected = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        "Set-Cookie: a=1\r\n"
        "Set-Cookie: b=2\r\n"
        "Set-Cookie: c=3\r\n"
    )
    assert formatter.format_headers(raw) == expected


def test_single_header_line_no_sorting_needed():
    """If only the status line is present, the output should be unchanged."""
    formatter = HeadersFormatter(format_options={"headers": {"sort": True}})
    raw = "HTTP/1.1 204 No Content\r\n"
    assert formatter.format_headers(raw) == raw
