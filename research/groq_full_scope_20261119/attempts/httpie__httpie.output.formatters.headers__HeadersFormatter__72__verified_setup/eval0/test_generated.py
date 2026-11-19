import pytest
from httpie.output.formatters.headers import HeadersFormatter


def test_headers_sorting_and_order(tmp_path):
    """
    Verify that HeadersFormatter sorts header lines by name while preserving
    the relative order of headers with the same name.
    """
    # Prepare a header block with unsorted lines and duplicate header names
    raw_headers = (
        "HTTP/1.1 200 OK\r\n"
        "b: second\r\n"
        "a: first\r\n"
        "b: third\r\n"
        "c: last\r\n"
    )
    formatter = HeadersFormatter()
    # Ensure the formatter is enabled (default sort option is True)
    assert formatter.enabled is True

    formatted = formatter.format_headers(raw_headers)
    # The first line (status line) should remain unchanged
    assert formatted.splitlines()[0] == "HTTP/1.1 200 OK"

    # The remaining lines should be sorted by header name
    expected_order = [
        "a: first",
        "b: second",
        "b: third",
        "c: last",
    ]
    assert formatted.splitlines()[1:] == expected_order


def test_headers_with_same_name_preserve_relative_order():
    """
    When multiple headers share the same name, their relative order should
    remain unchanged after sorting.
    """
    raw_headers = (
        "HTTP/1.1 200 OK\r\n"
        "x: first\r\n"
        "y: second\r\n"
        "x: third\r\n"
        "y: fourth\r\n"
    )
    formatter = HeadersFormatter()
    formatted = formatter.format_headers(raw_headers)
    # After sorting, 'x' headers should appear before 'y' headers,
    # but the order of 'x' and 'y' headers among themselves should be preserved.
    expected = [
        "x: first",
        "x: third",
        "y: second",
        "y: fourth",
    ]
    assert formatted.splitlines()[1:] == expected


def test_empty_header_block_returns_empty_string():
    """
    Passing an empty string to format_headers should return an empty string
    without raising an exception.
    """
    formatter = HeadersFormatter()
    assert formatter.format_headers("") == ""
