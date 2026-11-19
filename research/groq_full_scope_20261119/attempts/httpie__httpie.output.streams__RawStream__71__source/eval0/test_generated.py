import pytest
from httpie.output.streams import RawStream


class DummyMessage:
    """A minimal HTTPMessage stub that yields a body in chunks."""

    def __init__(self, body: bytes, chunk_size: int = 1024):
        self.body = body
        self.chunk_size = chunk_size

    def iter_body(self, chunk_size: int):
        """Yield the body in chunks of the requested size."""
        for i in range(0, len(self.body), chunk_size):
            yield self.body[i : i + chunk_size]


def test_rawstream_default_chunk_size(tmp_path):
    """RawStream should use the default CHUNK_SIZE and yield the full body."""
    body = b"Hello, world!" * 100  # 1300 bytes
    msg = DummyMessage(body)
    stream = RawStream(msg=msg)
    chunks = list(stream.iter_body())
    # With default chunk size 100KB, the body should be yielded in one chunk
    assert len(chunks) == 1
    assert chunks[0] == body


def test_rawstream_custom_chunk_size(tmp_path):
    """RawStream should respect a custom chunk size and split the body accordingly."""
    body = b"abc" * 500  # 1500 bytes
    msg = DummyMessage(body)
    stream = RawStream(chunk_size=200, msg=msg)
    chunks = list(stream.iter_body())
    # 1500 bytes with 200-byte chunks should produce 8 chunks (7 full + 1 partial)
    assert len(chunks) == 8
    assert chunks[-1] == body[7 * 200 :]


def test_rawstream_iter_body_raises(tmp_path):
    """If the underlying message raises an exception, RawStream should propagate it."""
    class FailingMessage:
        def iter_body(self, chunk_size: int):
            raise RuntimeError("failed to read body")

    msg = FailingMessage()
    stream = RawStream(msg=msg)
    with pytest.raises(RuntimeError, match="failed to read body"):
        list(stream.iter_body())
