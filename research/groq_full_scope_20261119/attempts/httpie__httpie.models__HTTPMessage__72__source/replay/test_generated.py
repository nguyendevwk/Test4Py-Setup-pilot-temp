import pytest
import requests
from httpie.models import HTTPMessage
from urllib.parse import urlsplit


class DummyHTTPMessage(HTTPMessage):
    """Concrete implementation of HTTPMessage for testing purposes."""

    def iter_body(self, chunk_size: int):
        return iter([b"chunk1", b"chunk2"])

    def iter_lines(self, chunk_size: int):
        return iter([(b"line1", b"\n"), (b"line2", b"\n")])

    @property
    def headers(self) -> str:
        return "\r\n".join(f"{k}: {v}" for k, v in self._orig.headers.items())

    @property
    def metadata(self) -> str:
        return f"URL: {self._orig.url}"


def _make_response(content_type: str):
    """Helper to create a requests.Response with a given Content-Type header."""
    resp = requests.Response()
    resp.status_code = 200
    resp.url = "http://example.com"
    resp._content = b"test"
    resp.headers["Content-Type"] = content_type
    return resp


def test_encoding_with_charset():
    """When Content-Type includes a charset, encoding property returns it."""
    resp = _make_response("text/plain; charset=utf-8")
    msg = DummyHTTPMessage(resp)
    assert msg.encoding == "utf-8"


def test_encoding_without_charset():
    """When Content-Type has no charset, encoding property returns empty string."""
    resp = _make_response("application/json")
    msg = DummyHTTPMessage(resp)
    assert msg.encoding == ""


def test_content_type_bytes():
    """Content-Type header may be bytes; property decodes it correctly."""
    resp = _make_response(b"application/xml; charset=iso-8859-1")
    msg = DummyHTTPMessage(resp)
    assert msg.content_type == "application/xml; charset=iso-8859-1"
