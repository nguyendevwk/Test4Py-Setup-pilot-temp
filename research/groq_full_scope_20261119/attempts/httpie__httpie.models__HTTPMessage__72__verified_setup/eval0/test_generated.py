import pytest
from httpie.models import HTTPMessage
from urllib.parse import urlsplit

# Minimal concrete implementation for testing purposes
class DummyHTTPMessage(HTTPMessage):
    def iter_body(self, chunk_size: int):
        return iter([b"part1", b"part2"])

    def iter_lines(self, chunk_size: int):
        return iter([(b"line1", b"\n"), (b"line2", b"\r\n")])

    @property
    def headers(self) -> str:
        return "\r\n".join(f"{k}: {v}" for k, v in self._orig.headers.items())

    @property
    def metadata(self) -> str:
        return f"URL: {self._orig.url}"


def test_content_type_string_header():
    """Content-Type header is a string; encoding should be empty."""
    class Orig:
        headers = {"Content-Type": "application/json"}
        url = "http://example.com"
    msg = DummyHTTPMessage(Orig())
    assert msg.content_type == "application/json"
    assert msg.encoding == ""  # no charset specified


def test_content_type_bytes_header_and_encoding():
    """Content-Type header is bytes; encoding should be extracted."""
    class Orig:
        headers = {"Content-Type": b"text/html; charset=utf-8"}
        url = "http://example.com"
    msg = DummyHTTPMessage(Orig())
    assert msg.content_type == "text/html; charset=utf-8"
    assert msg.encoding == "utf-8"


def test_headers_and_metadata_output():
    """Headers property returns correct string; metadata includes URL."""
    class Orig:
        headers = {"Host": "example.com", "Accept": "text/plain"}
        url = "https://example.com/path"
    msg = DummyHTTPMessage(Orig())
    expected_headers = "Host: example.com\r\nAccept: text/plain"
    assert msg.headers == expected_headers
    assert msg.metadata == "URL: https://example.com/path"
