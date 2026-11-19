import pytest
import requests
from urllib3.util import SKIP_HEADER, SKIPPABLE_HEADERS
from httpie.models import HTTPRequest

def test_headers_includes_request_line_and_host(tmp_path):
    # Create a request without Host header
    req = requests.Request(
        method="GET",
        url="http://example.com/path?query=1",
        headers={"User-Agent": "test-agent"},
    )
    prepared = req.prepare()
    http_req = HTTPRequest(prepared)

    headers_str = http_req.headers
    # The request line should be first
    assert headers_str.startswith("GET /path?query=1 HTTP/1.1")
    # Host header should be added automatically
    assert "Host: example.com" in headers_str
    # User-Agent should be present
    assert "User-Agent: test-agent" in headers_str

def test_headers_skips_skippable_header(tmp_path):
    # Create a request with a skippable header set to SKIP_HEADER
    req = requests.Request(
        method="POST",
        url="https://example.org",
        headers={"Connection": SKIP_HEADER, "Accept": "application/json"},
    )
    prepared = req.prepare()
    http_req = HTTPRequest(prepared)

    headers_str = http_req.headers
    # Skippable header should not appear
    assert "Connection:" not in headers_str
    # Accept header should appear
    assert "Accept: application/json" in headers_str

def test_body_encoding_and_iter_body(tmp_path):
    # Body as a string should be encoded to bytes
    req = requests.Request(
        method="POST",
        url="https://example.org",
        data="string body",
    )
    prepared = req.prepare()
    http_req = HTTPRequest(prepared)

    # Body property should return bytes
    assert isinstance(http_req.body, bytes)
    assert http_req.body == b"string body"

    # iter_body should yield the body once
    chunks = list(http_req.iter_body(chunk_size=10))
    assert chunks == [b"string body"]
