import threading
import pytest
from httpie.uploads import ChunkedMultipartUploadStream

class DummyEncoder:
    """A simple encoder that returns a fixed byte string in chunks."""
    def __init__(self, data: bytes, chunk_size: int = 10):
        self._data = data
        self._pos = 0
        self._chunk_size = chunk_size

    def read(self, size: int) -> bytes:
        if self._pos >= len(self._data):
            return b''
        end = min(self._pos + size, len(self._data))
        chunk = self._data[self._pos:end]
        self._pos = end
        return chunk

def test_chunked_upload_stream_yields_chunks():
    data = b"abcdefghijklmnopqrstuvwxyz"
    encoder = DummyEncoder(data, chunk_size=5)
    stream = ChunkedMultipartUploadStream(encoder)
    chunks = list(stream)
    assert chunks == [b"abcde", b"fghij", b"klmno", b"pqrst", b"uvwxy", b"z"]

def test_chunked_upload_stream_with_event_sets_event():
    data = b"12345"
    encoder = DummyEncoder(data, chunk_size=2)
    event = threading.Event()
    stream = ChunkedMultipartUploadStream(encoder, event=event)
    chunks = []
    for chunk in stream:
        chunks.append(chunk)
        assert event.is_set(), "Event should be set after each read"
        event.clear()
    assert chunks == [b"12", b"34", b"5"]

def test_chunked_upload_stream_handles_empty_encoder():
    encoder = DummyEncoder(b"", chunk_size=10)
    stream = ChunkedMultipartUploadStream(encoder)
    chunks = list(stream)
    assert chunks == [], "Empty encoder should produce no chunks"
