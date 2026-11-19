import pytest
import requests
from httpie.models import HTTPRequest
from urllib.parse import urlparse

# Helper to create a prepared request object
def make_prepared(method, url, headers=None, data=None):
    req = requests.Request(method=method, url=url, headers=headers, data=data)
    return req.prepare()

def test_headers_property_includes_request_line_and_host():
    url = "http://example.com/api?x=1"
    headers = {"User-Agent": "test-agent", "Accept": "application/json"}
    prepared = make_prepared("GET", url, headers=headers)
    http_req = HTTPRequest(prepared)

    hdrs = http_req.headers.split("\r\n")
    # First line should be the request line
    assert hdrs[0] == "GET /api?x=1 HTTP/1.1"
    # Host header should be present
    host_line = next((h for h in hdrs if h.startswith("Host:")), None)
    assert host_line is not None
    assert host_line == "Host: example.com"
    # Original headers should be present
    assert any(h.startswith("User-Agent:") for h in hdrs)
    assert any(h.startswith("Accept:") for h in hdrs)

def test_body_property_encodes_string_and_returns_bytes():
    data_str = '{"key":"value"}'
    prepared = make_prepared("POST", "http://example.com", data=data_str)
    http_req = HTTPRequest(prepared)

    body = http_req.body
    assert isinstance(body, bytes)
    assert body == data_str.encode()

    # When body is already bytes, it should be returned unchanged
    data_bytes = b"raw bytes"
    prepared2 = make_prepared("POST", "http://example.com", data=data_bytes)
    http_req2 = HTTPRequest(prepared2)
    assert http_req2.body is data_bytes

def test_iter_body_and_iter_lines_yield_correct_chunks():
    data = "chunked data"
    prepared = make_prepared("PUT", "http://example.com", data=data)
    http_req = HTTPRequest(prepared)

    # iter_body should yield the entire body once
    body_chunks = list(http_req.iter_body(chunk_size=10))
    assert body_chunks == [data.encode()]

    # iter_lines should yield a tuple of (body, b'')
    lines = list(http_req.iter_lines(chunk_size=10))
    assert lines == [(data.encode(), b'')]
