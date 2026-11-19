import pytest
import requests
from httpie.models import HTTPRequest
from urllib3.util import SKIP_HEADER, SKIPPABLE_HEADERS

def test_headers_includes_host_and_skips_header():
    # Prepare a request without a Host header and with a skip header
    req = requests.Request(
        method="GET",
        url="http://example.com/api?x=1",
        headers={
            "User-Agent": "test-agent",
            "X-Custom": "value",
            "X-Skip": SKIP_HEADER,  # header that should be skipped
        },
        data=None,
    )
    prepared = req.prepare()
    http_req = HTTPRequest(prepared)

    headers_str = http_req.headers
    # The request line should be first
    assert headers_str.startswith("GET /api?x=1 HTTP/1.1")
    # Host header should be added automatically
    assert "Host: example.com" in headers_str
    # Skippable header should not appear
    assert "X-Skip:" not in headers_str
    # Other headers should appear
    assert "User-Agent: test-agent" in headers_str
    assert "X-Custom: value" in headers_str

def test_body_encoding_and_iter_body():
    # Prepare a request with a string body
    req = requests.Request(
        method="POST",
        url="http://example.com/submit",
        headers={"Content-Type": "application/json"},
        data='{"key":"value"}',
    )
    prepared = req.prepare()
    http_req = HTTPRequest(prepared)

    # Body should be encoded to bytes
    assert http_req.body == b'{"key":"value"}'
    # iter_body should yield the body once
    chunks = list(http_req.iter_body(chunk_size=1024))
    assert chunks == [b'{"key":"value"}']

def test_empty_body_and_iter_lines():
    # Prepare a request with no body
    req = requests.Request(
        method="DELETE",
        url="http://example.com/resource/1",
        headers={"Accept": "application/json"},
        data=None,
    )
    prepared = req.prepare()
    http_req = HTTPRequest(prepared)

    # Body should be empty bytes
    assert http_req.body == b''
    # iter_body should yield empty bytes
    assert list(http_req.iter_body(chunk_size=512)) == [b'']
    # iter_lines should yield a tuple of (body, b'')
    assert list(http_req.iter_lines(chunk_size=512)) == [(b'', b'')]
