import pytest
from httpie.output.formatters.headers import HeadersFormatter


def test_sorting_of_headers():
    """Headers should be sorted alphabetically by name, preserving the first line."""
    raw = (
        "HTTP/1.1 200 OK\r\n"
        "b-Header: 2\r\n"
        "a-Header: 1\r\n"
        "c-Header: 3\r\n"
    )
    formatter = HeadersFormatter()
    formatted = formatter.format_headers(raw)
    expected = (
        "HTTP/1.1 200 OK\r\n"
        "a-Header: 1\r\n"
        "b-Header: 2\r\n"
        "c-Header: 3\r\n"
    )
    assert formatted == expected


def test_same_name_order_preserved():
    """Headers with the same name should keep their relative order after sorting."""
    raw = (
        "HTTP/1.1 200 OK\r\n"
        "X-Token: first\r\n"
        "A-Header: 1\r\n"
        "X-Token: second\r\n"
        "B-Header: 2\r\n"
    )
    formatter = HeadersFormatter()
    formatted = formatter.format_headers(raw)
    expected = (
        "HTTP/1.1 200 OK\r\n"
        "A-Header: 1\r\n"
        "B-Header: 2\r\n"
        "X-Token: first\r\n"
        "X-Token: second\r\n"
    )
    assert formatted == expected


def test_empty_and_single_header_cases(tmp_path):
    """Formatting should handle empty header blocks and single header lines gracefully."""
    # Empty headers (only first line)
    raw_empty = "HTTP/1.1 204 No Content\r\n"
    formatter = HeadersFormatter()
    assert formatter.format_headers(raw_empty) == raw_empty

    # Single header line
    raw_single = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
    )
    expected_single = raw_single
    assert formatter.format_headers(raw_single) == expected_single

    # Write to a temporary file and read back to ensure no file I/O errors
    file_path = tmp_path / "headers.txt"
    file_path.write_text(raw_single)
    file_content = file_path.read_text()
    assert formatter.format_headers(file_content) == expected_single
