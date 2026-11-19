import pytest
import requests
from httpie.models import HTTPRequest
from urllib3.util import SKIP_HEADER, SKIPPABLE_HEADERS

def test_headers_includes_request_line_and_host():
    # Build a request without a Host header
    req = requests.Request(
        method='GET',
        url='http://example.com/path?query=1',
        headers={'User-Agent': 'test-agent'}
    )
    wrapped = HTTPRequest(req.prepare())
    headers = wrapped.headers.split('\r\n')
    # First line should be the request line
    assert headers[0] == 'GET /path?query=1 HTTP/1.1'
    # Host header should be added automatically
    host_header = next(h for h in headers if h.startswith('Host:'))
    assert host_header == 'Host: example.com'
    # User-Agent should be present
    assert any(h.startswith('User-Agent:') for h in headers)

def test_body_encoding_and_iter_body():
    # Body as a string should be encoded to bytes
    req = requests.Request(
        method='POST',
        url='https://example.com',
        data='{"key":"value"}',
        headers={'Content-Type': 'application/json'}
    )
    wrapped = HTTPRequest(req.prepare())
    # body property should return bytes
    assert isinstance(wrapped.body, bytes)
    assert wrapped.body == b'{"key":"value"}'
    # iter_body should yield the same bytes
    chunks = list(wrapped.iter_body(chunk_size=1024))
    assert chunks == [b'{"key":"value"}']

def test_skippable_headers_are_filtered():
    # Include a skippable header with SKIP_HEADER value
    req = requests.Request(
        method='GET',
        url='https://example.com',
        headers={'Connection': SKIP_HEADER, 'Accept': 'text/html'}
    )
    wrapped = HTTPRequest(req.prepare())
    headers = wrapped.headers.split('\r\n')
    # The skippable header should not appear
    assert not any(h.startswith('Connection:') for h in headers)
    # Non-skippable header should appear
    assert any(h.startswith('Accept:') for h in headers)
