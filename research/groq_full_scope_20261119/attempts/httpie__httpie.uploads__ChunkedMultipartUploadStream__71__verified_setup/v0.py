import threading
import pytest
from httpie.uploads import ChunkedMultipartUploadStream


class DummyEncoder:
    """Simple encoder that yields predefined byte chunks."""
    def __init__(self, data: bytes, chunk_size: int = 10):
        self._data = data
        self._pos = 0
        self._chunk_size = chunk_size

    def read(self, size: int):
        if self._pos >= len(self._data):
            return b""
        chunk = self._data[self._pos : self._pos + size]
        self._pos += size
        return chunk


def test_chunked_stream_yields_expected_chunks(tmp_path):
    """Verify that the stream yields the correct chunks and stops."""
    data = b"abcdefghijklmnopqrstuvwxyz"
    encoder = DummyEncoder(data, chunk_size=5)
    stream = ChunkedMultipartUploadStream(encoder)
    chunks = list(stream)
    assert chunks == [b"abcde", b"fghij", b"klmno", b"pqrst", b"uvwxy", b"z"]
    # Ensure no extra empty chunk is yielded
    assert b"" not in chunks


def test_event_is_set_after_first_chunk(tmp_path):
    """Ensure the provided event is set after the first chunk is read."""
    data = b"1234567890"
    encoder = DummyEncoder(data, chunk_size=3)
    event = threading.Event()
    stream = ChunkedMultipartUploadStream(encoder, event=event)
    # Before iteration, event should not be set
    assert not event.is_set()
    # Consume first chunk
    first_chunk = next(iter(stream))
    assert first_chunk == b"123"
    # Event should now be set
    assert event.is_set()


def test_empty_encoder_yields_no_chunks(tmp_path):
    """When the encoder returns no data, the stream should yield nothing."""
    encoder = DummyEncoder(b"", chunk_size=4)
    stream = ChunkedMultipartUploadStream(encoder)
    assert list(stream) == []
