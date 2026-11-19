import threading
import pytest
from httpie.uploads import ChunkedMultipartUploadStream


class DummyEncoder:
    """Simple encoder that returns a fixed byte string in chunks."""
    def __init__(self, data: bytes, chunk_size: int = 10):
        self.data = data
        self.chunk_size = chunk_size
        self.pos = 0

    def read(self, size: int):
        if self.pos >= len(self.data):
            return b""
        end = min(self.pos + size, len(self.data))
        chunk = self.data[self.pos:end]
        self.pos = end
        return chunk


def test_chunked_stream_yields_correct_chunks():
    data = b"abcdefghijklmnopqrstuvwxyz"
    encoder = DummyEncoder(data, chunk_size=5)
    stream = ChunkedMultipartUploadStream(encoder)
    chunks = list(stream)
    assert chunks == [b"abcde", b"fghij", b"klmno", b"pqrst", b"uvwxy", b"z"]


def test_event_is_set_after_each_chunk():
    data = b"1234567890"
    encoder = DummyEncoder(data, chunk_size=3)
    event = threading.Event()
    stream = ChunkedMultipartUploadStream(encoder, event=event)
    # Ensure event is not set before iteration
    assert not event.is_set()
    # Consume first chunk
    first_chunk = next(iter(stream))
    assert first_chunk == b"123"
    # Event should be set after first read
    assert event.is_set()
    # Reset event for next chunk
    event.clear()
    # Consume remaining chunks
    rest_chunks = list(stream)
    assert rest_chunks == [b"456", b"789", b"0"]


def test_no_chunks_when_encoder_returns_empty():
    encoder = DummyEncoder(b"", chunk_size=10)
    stream = ChunkedMultipartUploadStream(encoder)
    chunks = list(stream)
    assert chunks == []
