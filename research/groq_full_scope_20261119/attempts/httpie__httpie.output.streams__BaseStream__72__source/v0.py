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

def test_headers_only_output(message):
    """When only headers are requested, the stream yields headers and a blank line."""
    opts = OutputOptions(headers=True, body=False, meta=False)
    stream = DummyStream(message, opts)
    result = b"".join(iter(stream))
    expected = message.headers.encode() + b"\r\n\r\n"
    assert result == expected

def test_body_only_output(message):
    """When only body is requested, the stream yields the body without headers or metadata."""
    opts = OutputOptions(headers=False, body=True, meta=False)
    stream = DummyStream(message, opts)
    result = b"".join(iter(stream))
    assert result == message.body.encode()

def test_full_output_with_metadata(message):
    """When headers, body, and metadata are requested, the stream yields all parts in order."""
    opts = OutputOptions(headers=True, body=True, meta=True)
    stream = DummyStream(message, opts)
    result = b"".join(iter(stream))
    expected = (
        message.headers.encode() + b"\r\n\r\n" +          # headers
        message.body.encode() + b"\n\n" +                # body + separator
        message.metadata.encode() + b"\n\n"              # metadata
    )
    assert result == expected
