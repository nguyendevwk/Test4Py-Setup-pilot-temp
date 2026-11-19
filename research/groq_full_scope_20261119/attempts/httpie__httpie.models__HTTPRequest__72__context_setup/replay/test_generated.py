import pytest
import requests
from httpie.models import HTTPRequest
from urllib.parse import urlsplit

def test_headers_includes_request_line_and_host():
    # Build a request without an explicit Host header
    req = requests.Request(
        method="GET",
        url="https://example.com/api?foo=bar",
        headers={"User-Agent": "test-agent"},
    )
    prepared = requests.Session().prepare_request(req)
    wrapped = HTTPRequest(prepared)

    headers_str = wrapped.headers
    # The request line should be first
    assert headers_str.startswith("GET /api?foo=bar HTTP/1.1")
    # Host header should be added automatically
    assert "Host: example.com" in headers_str
    # User-Agent header should be present
    assert "User-Agent: test-agent" in headers_str

def test_body_encoding_and_iter_body():
    # Body provided as a string should be encoded to bytes
    req = requests.Request(
        method="POST",
        url="https://example.com/submit",
        data="foo=bar",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    prepared = requests.Session().prepare_request(req)
    wrapped = HTTPRequest(prepared)

    # Body property should return bytes
    assert isinstance(wrapped.body, bytes)
    assert wrapped.body == b"foo=bar"

    # iter_body should yield the body once
    chunks = list(wrapped.iter_body(chunk_size=10))
    assert chunks == [b"foo=bar"]

def test_iter_lines_yields_body_and_empty_line_feed():
    # Body as bytes
    req = requests.Request(
        method="PUT",
        url="https://example.com/update",
        data=b"update data",
        headers={"Content-Type": "text/plain"},
    )
    prepared = requests.Session().prepare_request(req)
    wrapped = HTTPRequest(prepared)

    lines = list(wrapped.iter_lines(chunk_size=5))
    # Should yield a single tuple (body, empty line feed)
    assert lines == [(b"update data", b"")]
