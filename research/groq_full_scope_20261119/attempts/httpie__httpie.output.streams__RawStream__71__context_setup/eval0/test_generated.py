import pytest
from httpie.output.streams import RawStream, BaseStream, DataSuppressedError
from httpie.models import HTTPMessage, OutputOptions

# Helper message class for tests
class DummyMessage(HTTPMessage):
    def __init__(self, body: bytes, headers: str = "", metadata: str = ""):
        self._body = body
        self._headers = headers
        self._metadata = metadata

    def iter_body(self, chunk_size: int):
        for i in range(0, len(self._body), chunk_size):
            yield self._body[i:i+chunk_size]

    def headers(self):
        return self._headers

    def metadata(self):
        return self._metadata

    def encode(self):
        return self._body

    def headers_encode(self):
        return self._headers.encode()

    def metadata_encode(self):
        return self._metadata.encode()


def test_rawstream_iter_body_chunks():
    body = b"HelloWorld" * 10  # 100 bytes
    msg = DummyMessage(body=body)
    opts = OutputOptions(headers=False, body=True, meta=False)
    stream = RawStream(msg=msg, output_options=opts, chunk_size=20)
    chunks = list(stream.iter_body())
    assert all(len(chunk) <= 20 for chunk in chunks)
    assert b"".join(chunks) == body
    assert len(chunks) == 5  # 100 / 20


def test_rawstream_headers_and_metadata_inclusion():
    body = b"data"
    headers = "Content-Type: text/plain"
    metadata = "meta-info"
    msg = DummyMessage(body=body, headers=headers, metadata=metadata)
    opts = OutputOptions(headers=True, body=True, meta=True)
    stream = RawStream(msg=msg, output_options=opts)
    output = b"".join(stream)
    # Headers should appear first followed by CRLFCRLF
    assert output.startswith(headers.encode() + b"\r\n\r\n")
    # Body should follow
    assert body in output
    # Metadata should appear after two newlines following body
    assert metadata.encode() in output
    # Ensure order: headers, body, metadata
    assert output.index(body) > output.index(headers.encode())
    assert output.index(metadata.encode()) > output.index(body)


def test_rawstream_data_suppressed_error():
    class SuppressMessage(HTTPMessage):
        def iter_body(self, chunk_size: int):
            raise DataSuppressedError("Body suppressed")

        def headers(self):
            return "X-Test: 1"

        def metadata(self):
            return ""

    msg = SuppressMessage()
    opts = OutputOptions(headers=True, body=True, meta=False)
    stream = RawStream(msg=msg, output_options=opts)
    output = b"".join(stream)
    # Headers should be present
    assert b"X-Test: 1" in output
    # Suppressed message should be included
    assert b"Body suppressed" in output
    # No body chunks should be present
    assert b"\r\n\r\n" not in output.split(b"\r\n\r\n")[1]  # second part should be suppressed message only
