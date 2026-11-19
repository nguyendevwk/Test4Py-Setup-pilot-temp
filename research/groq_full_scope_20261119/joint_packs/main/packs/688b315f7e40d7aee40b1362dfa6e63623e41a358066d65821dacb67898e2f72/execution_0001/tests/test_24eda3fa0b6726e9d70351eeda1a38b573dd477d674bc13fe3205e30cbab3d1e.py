import pytest
import requests
from httpie.models import HTTPMessage
from urllib.parse import urlsplit

# Helper subclass that implements the abstract methods using a requests.Response
class DummyHTTPMessage(HTTPMessage):
    def __init__(self, response: requests.Response):
        super().__init__(response)

    def iter_body(self, chunk_size: int):
        data = self._orig.content
        for i in range(0, len(data), chunk_size):
            yield data[i:i+chunk_size]

    def iter_lines(self, chunk_size: int):
        data = self._orig.content
        start = 0
        while start < len(data):
            end = data.find(b'\n', start)
            if end == -1:
                line = data[start:]
                lf = b''
                start = len(data)
            else:
                line = data[start:end]
                lf = b'\n'
                start = end + 1
            yield (line, lf)

    @property
    def headers(self):
        return "\r\n".join(f"{k}: {v}" for k, v in self._orig.headers.items())

    @property
    def metadata(self):
        return f"URL: {self._orig.url} Status: {self._orig.status_code}"


def test_encoding_and_content_type(tmp_path):
    # Create a simple response with a known charset
    url = "http://example.com"
    resp = requests.Response()
    resp.url = url
    resp.status_code = 200
    resp._content = b"hello world"
    resp.headers = {"Content-Type": "text/plain; charset=utf-8"}
    msg = DummyHTTPMessage(resp)

    # content_type should return the header string
    assert msg.content_type == "text/plain; charset=utf-8"

    # encoding property should parse charset
    assert msg.encoding == "utf-8"

    # Changing the header should update encoding lazily
    resp.headers["Content-Type"] = "text/html"
    # cached_property should still return old value
    assert msg.encoding == "utf-8"
    # Invalidate cache by deleting attribute
    del msg.__dict__["encoding"]
    assert msg.encoding == ""


def test_iter_body_and_lines(tmp_path):
    # Response with multiple lines
    content = b"line1\nline2\nline3"
    resp = requests.Response()
    resp.url = "http://example.com"
    resp.status_code = 200
    resp._content = content
    resp.headers = {}
    msg = DummyHTTPMessage(resp)

    # iter_body should yield chunks of specified size
    chunks = list(msg.iter_body(5))
    assert chunks == [b"line1", b"\nline", b"2\nlin", b"e3"]

    # iter_lines should yield (line, line_feed) tuples
    lines = list(msg.iter_lines(10))
    assert lines == [
        (b"line1", b"\n"),
        (b"line2", b"\n"),
        (b"line3", b""),
    ]


def test_headers_and_metadata(tmp_path):
    resp = requests.Response()
    resp.url = "https://example.org/api"
    resp.status_code = 404
    resp._content = b"Not Found"
    resp.headers = {
        "Content-Type": "text/plain",
        "X-Custom": "value",
    }
    msg = DummyHTTPMessage(resp)

    # headers property should format headers correctly
    headers_str = msg.headers
    assert "Content-Type: text/plain" in headers_str
    assert "X-Custom: value" in headers_str
    assert "\r\n" in headers_str

    # metadata should include URL and status code
    meta = msg.metadata
    assert "URL: https://example.org/api" in meta
    assert "Status: 404" in meta
