import pytest
from httpie.output.streams import RawStream


class DummyMessage:
    """A minimal HTTPMessage stub that yields a body in chunks."""

    def __init__(self, body: bytes):
        self._body = body

    def iter_body(self, chunk_size: int):
        """Yield the body in chunks of the requested size."""
        for i in range(0, len(self._body), chunk_size):
            yield self._body[i : i + chunk_size]


def test_iter_body_normal_chunking():
    """RawStream should split the body into chunks of the specified size."""
    body = b"HelloWorld"
    msg = DummyMessage(body)
    stream = RawStream(msg=msg, chunk_size=5)
    chunks = list(stream.iter_body())
    assert chunks == [b"Hello", b"World"]
    assert all(isinstance(chunk, bytes) for chunk in chunks)


def test_iter_body_boundary_larger_than_body():
    """If the chunk size exceeds the body length, the entire body is returned as one chunk."""
    body = b"Short"
    msg = DummyMessage(body)
    stream = RawStream(msg=msg, chunk_size=100)
    chunks = list(stream.iter_body())
    assert chunks == [body]
    assert len(chunks) == 1


def test_iter_body_zero_chunk_size_raises():
    """Providing a non‑positive chunk size should raise a ValueError."""
    body = b"Data"
    msg = DummyMessage(body)
    with pytest.raises(ValueError):
        RawStream(msg=msg, chunk_size=0)
