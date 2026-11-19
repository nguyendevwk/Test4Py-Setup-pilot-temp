import pytest
from httpie.output.formatters.headers import HeadersFormatter

def test_sort_headers_normal():
    """Headers are sorted alphabetically by name, preserving the first line."""
    raw = (
        "HTTP/1.1 200 OK\r\n"
        "zeta: last\n"
        "alpha: first\n"
        "gamma: middle\n"
    )
    formatter = HeadersFormatter()
    formatted = formatter.format_headers(raw)
    expected = (
        "HTTP/1.1 200 OK\r\n"
        "alpha: first\n"
        "gamma: middle\n"
        "zeta: last"
    )
    assert formatted == expected

def test_sort_headers_duplicates_preserve_order():
    """Duplicate header names keep their relative order after sorting."""
    raw = (
        "HTTP/1.1 200 OK\r\n"
        "b: second\n"
        "a: first\n"
        "b: third\n"
        "a: fourth\n"
    )
    formatter = HeadersFormatter()
    formatted = formatter.format_headers(raw)
    expected = (
        "HTTP/1.1 200 OK\r\n"
        "a: first\n"
        "a: fourth\n"
        "b: second\n"
        "b: third"
    )
    assert formatted == expected

def test_sort_headers_single_header_and_enabled_flag():
    """Single header line remains unchanged and enabled flag reflects format_options."""
    raw = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html\n"
    )
    formatter = HeadersFormatter(format_options={'headers': {'sort': False}})
    formatted = formatter.format_headers(raw)
    assert formatted == raw
    assert formatter.enabled is False
