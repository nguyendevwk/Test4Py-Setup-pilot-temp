import threading
import pytest
from httpie.uploads import ChunkedMultipartUploadStream


class DummyEncoder:
    """Simple encoder that returns a fixed byte string in chunks."""
    def __init__(self, data: bytes, chunk_size: int = 10):
        self._data = data
        self._pos = 0
        self.chunk_size = chunk_size

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


def test_chunked_upload_stream_yields_chunks_and_sets_event():
    data = b"abcdefghijklmnopqrstuvwxyz"
    encoder = DummyEncoder(data, chunk_size=5)
    event = threading.Event()
    stream = ChunkedMultipartUploadStream(encoder, event=event)

    chunks = list(stream)
    assert chunks == [b"abcde", b"fghij", b"klmno", b"pqrst", b"uvwxy", b"z"]
    assert event.is_set()


def test_chunked_upload_stream_handles_exact_chunk_boundary():
    data = b"1234567890"  # 10 bytes, chunk_size default 100*1024 > data length
    encoder = DummyEncoder(data, chunk_size=10)
    stream = ChunkedMultipartUploadStream(encoder)

    chunks = list(stream)
    assert chunks == [b"1234567890"]


def test_chunked_upload_stream_propagates_encoder_exception():
    encoder = FailingEncoder()
    stream = ChunkedMultipartUploadStream(encoder)

    with pytest.raises(RuntimeError, match="read error"):
        list(stream)
