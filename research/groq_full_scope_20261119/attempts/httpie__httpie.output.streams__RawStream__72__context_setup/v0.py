import pytest
from httpie.output.streams import RawStream, BaseStream, DataSuppressedError
from httpie.models import HTTPMessage, OutputOptions

class DummyMessage(HTTPMessage):
    def __init__(self, body_bytes: bytes):
        self._body = body_bytes
        self.headers = b"Content-Type: text/plain"
        self.metadata = b"Dummy metadata"

    def iter_body(self, chunk_size: int):
        # Yield body in chunks of given size
        for i in range(0, len(self._body), chunk_size):
            yield self._body[i:i+chunk_size]

def test_rawstream_iter_body_chunks():
    body = b"abcdefghij" * 10  # 100 bytes
    msg = DummyMessage(body)
    stream = RawStream(msg=msg, output_options=OutputOptions(body=True))
    chunks = list(stream.iter_body())
    assert all(isinstance(c, bytes) for c in chunks)
    assert b"".join(chunks) == body
    # Ensure chunk size respected
    assert all(len(c) <= stream.CHUNK_SIZE for c in chunks)

def test_rawstream_full_iteration_with_headers_and_meta():
    body = b"hello world"
    msg = DummyMessage(body)
    opts = OutputOptions(headers=True, body=True, meta=True)
    stream = RawStream(msg=msg, output_options=opts)
    result = b"".join(stream)
    expected = (
        msg.headers + b"\r\n\r\n" +  # headers
        body + b"\n\n" +            # body + separator before meta
        msg.metadata + b"\n\n"      # metadata
    )
    assert result == expected

def test_rawstream_data_suppressed_error():
    class SuppressMessage(HTTPMessage):
        def __init__(self):
            self.headers = b"Content-Type: text/plain"
            self.metadata = b"Meta"
        def iter_body(self, chunk_size: int):
            raise DataSuppressedError("Body suppressed")

    msg = SuppressMessage()
    opts = OutputOptions(headers=True, body=True, meta=True)
    stream = RawStream(msg=msg, output_options=opts)
    result = b"".join(stream)
    expected = (
        msg.headers + b"\r\n\r\n" +  # headers
        b"\n" +                      # newline after suppressed body
        b"Body suppressed" + b"\n\n" +  # suppressed message + separator
        msg.metadata + b"\n\n"      # metadata
    )
    assert result == expected
