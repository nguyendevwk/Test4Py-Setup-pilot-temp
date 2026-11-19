import threading
import pytest
from httpie.uploads import ChunkedMultipartUploadStream

class DummyEncoder:
    """Simple encoder that returns a fixed byte string in chunks."""
    def __init__(self, data: bytes, chunk_size: int = 10):
        self._data = data
        self._pos = 0
        self._chunk_size = chunk_size

    def read(self, size: int) -> bytes:
        if self._pos >= len(self._data):
            return b""
        end = min(self._pos + size, len(self._data))
        chunk = self._data[self._pos:end]
        self._pos = end
        return chunk

class FailingEncoder:
    """Encoder that raises an exception on read."""
    def read(self, size: int):
        raise RuntimeError("read error")

def test_chunked_stream_yields_expected_chunks():
    data = b"abcdefghijklmnopqrstuvwxyz"
    encoder = DummyEncoder(data, chunk_size=5)
    stream = ChunkedMultipartUploadStream(encoder)
    chunks = list(stream)
    assert chunks == [b"abcde", b"fghij", b"klmno", b"pqrst", b"uvwxy", b"z"]
    # Ensure that the encoder was exhausted
    assert encoder.read(1) == b""

def test_chunked_stream_sets_event_for_each_chunk():
    data = b"1234567890"
    encoder = DummyEncoder(data, chunk_size=3)
    event = threading.Event()
    stream = ChunkedMultipartUploadStream(encoder, event=event)
    # The event should be set after the first chunk
    chunks = []
    for chunk in stream:
        chunks.append(chunk)
        assert event.is_set()
        event.clear()
    assert chunks == [b"123", b"456", b"789", b"0"]

def test_chunked_stream_propagates_encoder_errors():
    encoder = FailingEncoder()
    stream = ChunkedMultipartUploadStream(encoder)
    with pytest.raises(RuntimeError, match="read error"):
        list(stream)
