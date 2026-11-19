import pytest
from httpie.output.streams import BaseStream, DataSuppressedError
from httpie.models import HTTPMessage, OutputOptions
from httpie.encoding import UTF8


class DummyMessage(HTTPMessage):
    def __init__(self, headers: str, body: bytes, metadata: str):
        self._headers = headers
        self._body = body
        self._metadata = metadata

    def headers(self) -> str:
        return self._headers

    def body(self) -> bytes:
        return self._body

    def metadata(self) -> str:
        return self._metadata

    def encode(self) -> bytes:
        return self._body

    def headers_encode(self) -> bytes:
        return self._headers.encode(UTF8)

    def metadata_encode(self) -> bytes:
        return self._metadata.encode(UTF8)


class DummyStream(BaseStream):
    def iter_body(self):
        return iter(self.msg.body())


def test_stream_normal_output():
    msg = DummyMessage(
        headers="HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n",
        body=b"Hello, world!",
        metadata="Request: GET /",
    )
    opts = OutputOptions(headers=True, body=True, meta=True)
    chunks = list(DummyStream(msg, opts))
    # headers + double CRLF
    assert chunks[0] == msg.headers.encode(UTF8)
    assert chunks[1] == b"\r\n\r\n"
    # body
    assert chunks[2] == b"Hello, world!"
    # meta preceded by two newlines
    assert chunks[3] == b"\n\n"
    assert chunks[4] == msg.metadata.encode(UTF8)
    assert chunks[5] == b"\n\n"


def test_stream_no_body_only_headers():
    msg = DummyMessage(
        headers="HTTP/1.1 204 No Content\r\n",
        body=b"",
        metadata="",
    )
    opts = OutputOptions(headers=True, body=False, meta=False)
    chunks = list(DummyStream(msg, opts))
    assert chunks == [msg.headers.encode(UTF8), b"\r\n\r\n"]


def test_stream_body_suppressed_error():
    class SuppressStream(BaseStream):
        def iter_body(self):
            raise DataSuppressedError("Body suppressed")

    msg = DummyMessage(
        headers="HTTP/1.1 200 OK\r\n",
        body=b"ignored",
        metadata="",
    )
    opts = OutputOptions(headers=True, body=True, meta=False)
    stream = SuppressStream(msg, opts)
    chunks = list(stream)
    # headers + double CRLF
    assert chunks[0] == msg.headers.encode(UTF8)
    assert chunks[1] == b"\r\n\r\n"
    # suppressed message
    assert chunks[2] == b"Body suppressed"
