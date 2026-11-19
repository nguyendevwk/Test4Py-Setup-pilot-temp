import pytest
from httpie.models import HTTPMessage
from urllib3.util import SKIP_HEADER, SKIPPABLE_HEADERS

class DummyMessage(HTTPMessage):
    def __init__(self, headers, body=b""):
        super().__init__(self)
        self._orig = type("orig", (), {"headers": headers, "content": body})()

    def iter_body(self, chunk_size: int):
        yield self._orig.content

    def iter_lines(self, chunk_size: int):
        yield (self._orig.content, b"\n")

    @property
    def headers(self):
        return "\n".join(f"{k}: {v}" for k, v in self._orig.headers.items())

    @property
    def metadata(self):
        return ""

def test_encoding_from_charset_header():
    headers = {"Content-Type": "text/plain; charset=utf-8"}
    msg = DummyMessage(headers)
    assert msg.content_type == "text/plain; charset=utf-8"
    assert msg.encoding == "utf-8"

def test_encoding_with_bytes_header():
    headers = {"Content-Type": b"text/html; charset=iso-8859-1"}
    msg = DummyMessage(headers)
    assert msg.content_type == "text/html; charset=iso-8859-1"
    assert msg.encoding == "iso-8859-1"

def test_encoding_missing_header():
    headers = {}
    msg = DummyMessage(headers)
    assert msg.content_type == ""
    assert msg.encoding == ""
