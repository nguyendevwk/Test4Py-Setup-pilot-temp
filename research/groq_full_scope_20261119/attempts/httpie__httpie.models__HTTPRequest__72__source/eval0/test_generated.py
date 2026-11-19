import requests
from httpie.models import HTTPRequest
from urllib3.util import SKIP_HEADER, SKIPPABLE_HEADERS


def test_headers_includes_request_line_and_host(tmp_path):
    # Build a request without an explicit Host header
    req = requests.Request(
        method="GET",
        url="http://example.com/path?query=1",
        headers={"User-Agent": "test-agent"},
    )
    prepared = req.prepare()
    http_req = HTTPRequest(prepared)

    headers = http_req.headers.split("\r\n")
    # First line should be the request line
    assert headers[0] == "GET /path?query=1 HTTP/1.1"
    # Host header should be added automatically
    host_header = next(h for h in headers if h.lower().startswith("host:"))
    assert host_header == "Host: example.com"
    # User-Agent should be present
    assert any(h.startswith("User-Agent:") for h in headers)


def test_body_encodes_string_and_iter_body(tmp_path):
    # Body provided as a string
    req = requests.Request(
        method="POST",
        url="http://example.com",
        data="json payload",
    )
    prepared = req.prepare()
    http_req = HTTPRequest(prepared)

    # Body property should return bytes
    assert isinstance(http_req.body, bytes)
    assert http_req.body == b"json payload"

    # iter_body should yield the body once
    chunks = list(http_req.iter_body(chunk_size=10))
    assert chunks == [b"json payload"]


def test_headers_skip_skippable_headers(tmp_path):
    # Include a skippable header with SKIP_HEADER value
    req = requests.Request(
        method="GET",
        url="http://example.com",
        headers={"Connection": SKIP_HEADER, "Accept": "text/plain"},
    )
    prepared = req.prepare()
    http_req = HTTPRequest(prepared)

    headers = http_req.headers.split("\r\n")
    # Connection header should be omitted
    assert not any(h.lower().startswith("connection:") for h in headers)
    # Accept header should be present
    assert any(h.startswith("Accept:") for h in headers)
