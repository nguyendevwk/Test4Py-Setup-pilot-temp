import pytest
from httpie.output.formatters.headers import HeadersFormatter


def test_headers_sorting_and_stability(tmp_path):
    """HeadersFormatter should sort headers by name while preserving the order of
    headers with the same name."""
    formatter = HeadersFormatter(format_options={"headers": {"sort": True}})
    raw_headers = (
        "HTTP/1.1 200 OK\n"
        "b: second\n"
        "a: first\n"
        "b: third\n"
        "c: last\n"
    )
    expected = (
        "HTTP/1.1 200 OK\r\n"
        "a: first\r\n"
        "b: second\r\n"
        "b: third\r\n"
        "c: last"
    )
    assert formatter.format_headers(raw_headers) == expected
    assert formatter.enabled is True


def test_headers_empty_input(tmp_path):
    """An empty string should return an empty string without errors."""
    formatter = HeadersFormatter(format_options={"headers": {"sort": True}})
    assert formatter.format_headers("") == ""


def test_headers_invalid_input_raises_type_error(tmp_path):
    """Passing a non-string should raise a TypeError."""
    formatter = HeadersFormatter(format_options={"headers": {"sort": True}})
    with pytest.raises(TypeError):
        formatter.format_headers(None)
