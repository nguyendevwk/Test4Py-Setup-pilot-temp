import pytest
from httpie.output.formatters.headers import HeadersFormatter

def test_headers_sorting_and_duplicate_order(tmp_path):
    # Prepare a header string with unsorted headers and duplicate names
    raw_headers = (
        "HTTP/1.1 200 OK\r\n"
        "z-Header: last\r\n"
        "a-Header: first\r\n"
        "m-Header: middle\r\n"
        "a-Header: second\r\n"
        "z-Header: another\r\n"
    )
    formatter = HeadersFormatter()
    formatted = formatter.format_headers(raw_headers)

    # Split into lines and verify the first line is unchanged
    lines = formatted.split("\r\n")
    assert lines[0] == "HTTP/1.1 200 OK"

    # The remaining lines should be sorted by header name, preserving relative order of duplicates
    expected_order = [
        "a-Header: first",
        "a-Header: second",
        "m-Header: middle",
        "z-Header: last",
        "z-Header: another",
    ]
    assert lines[1:] == expected_order

def test_headers_no_header_lines(tmp_path):
    # Only a status line, no header lines
    raw_headers = "HTTP/1.1 204 No Content\r\n"
    formatter = HeadersFormatter()
    formatted = formatter.format_headers(raw_headers)

    # The output should be identical to the input
    assert formatted == raw_headers

def test_headers_enabled_flag_set_from_format_options():
    # Provide custom format_options to control the enabled flag
    custom_options = {"headers": {"sort": False}}
    formatter = HeadersFormatter(format_options=custom_options)
    assert formatter.enabled is False

    # Changing the option should reflect in the enabled flag
    custom_options = {"headers": {"sort": True}}
    formatter = HeadersFormatter(format_options=custom_options)
    assert formatter.enabled is True
