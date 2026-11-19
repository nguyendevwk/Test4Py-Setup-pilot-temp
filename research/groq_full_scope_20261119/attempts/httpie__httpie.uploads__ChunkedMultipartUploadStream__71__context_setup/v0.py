import threading
import pytest
from httpie.uploads import ChunkedMultipartUploadStream

class DummyEncoder:
    """Simple encoder that returns a fixed byte string in chunks."""
    def __init__(self, data: bytes, chunk_size: int = 10):
        self._data = data
        self._pos = 0
        self.chunk_size = chunk_size

    def read(self, size: int):
        if self._pos >= len(self._data):
            return b''
        chunk = self._data[self._pos : self._pos + size]
        self._pos += size
        return chunk

def test_iteration_yields_chunks():
    data = b'abcdefghijklmnopqrstuvwxyz'
    encoder = DummyEncoder(data, chunk_size=5)
    stream = ChunkedMultipartUploadStream(encoder)
    chunks = list(stream)
    # The encoder should split the data into 5-byte chunks
    assert chunks == [b'abcde', b'fghij', b'klmno', b'pqrst', b'uvwxy', b'z']

def test_event_set_on_each_chunk():
    data = b'1234567890'
    encoder = DummyEncoder(data, chunk_size=3)
    event = threading.Event()
    stream = ChunkedMultipartUploadStream(encoder, event=event)
    # Initially the event should not be set
    assert not event.is_set()
    # Consume the first chunk
    first_chunk = next(iter(stream))
    # After reading a chunk the event should be set
    assert event.is_set()
    # Reset the event for the next chunk
    event.clear()
    # Consume the second chunk
    second_chunk = next(iter(stream))
    assert event.is_set()
    # Ensure the chunks are correct
    assert first_chunk == b'123'
    assert second_chunk == b'456'

def test_empty_encoder_yields_no_chunks():
    encoder = DummyEncoder(b'', chunk_size=10)
    stream = ChunkedMultipartUploadStream(encoder)
    # Converting to list should give an empty list
    assert list(stream) == []
