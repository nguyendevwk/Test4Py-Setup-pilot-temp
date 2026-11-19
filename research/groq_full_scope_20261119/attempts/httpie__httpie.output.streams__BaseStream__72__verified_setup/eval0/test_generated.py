import pytest
from httpie.output.streams import BaseStream
from httpie.models import HTTPMessage, OutputOptions

# Minimal concrete implementation of BaseStream for testing
class DummyStream(BaseStream):
    def iter_body(self):
        # Return body as a single chunk
        return [b"Hello, world!"]

# Helper to create a simple HTTPMessage
class SimpleMessage(HTTPMessage):
    def __init__(self, headers: str, metadata: str, body: str):
        self._headers = headers
        self._metadata = metadata
        self._body = body

    def headers(self):
        return self._headers

    def metadata(self):
        return self._metadata

    def body(self):
        return self._body

    def encode(self):
        return self._body.encode()

    def headers_encode(self):
        return self._headers.encode()

    def metadata_encode(self):
        return self._metadata.encode()

    # Provide attributes expected by BaseStream
    @property
    def headers(self):
        return self._headers

    @property
    def metadata(self):
        return self._metadata

    @property
    def body(self):
        return self._body

@pytest.fixture
def message():
    return SimpleMessage(
        headers="HTTP/1.1 200 OK\r\nContent-Type: text/plain",
        metadata="Request: GET /",
        body="Hello, world!"
    )

def test_headers_only(message):
    opts = OutputOptions(headers=True, body=False, meta=False)
    stream = DummyStream(message, opts)
    result = b"".join(stream)
    assert result == b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n"

def test_body_only(message):
    opts = OutputOptions(headers=False, body=True, meta=False)
    stream = DummyStream(message, opts)
    result = b"".join(stream)
    assert result == b"Hello, world!"

def test_headers_body_meta(message):
    opts = OutputOptions(headers=True, body=True, meta=True)
    stream = DummyStream(message, opts)
    result = b"".join(stream)
    expected = (
        b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n"
        b"Hello, world!\n\n"
        b"Request: GET /\n\n"
    )
    assert result == expected
