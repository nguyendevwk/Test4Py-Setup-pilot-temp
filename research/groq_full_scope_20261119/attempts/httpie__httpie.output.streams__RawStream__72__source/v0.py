import pytest
from httpie.output.streams import RawStream


class DummyMessage:
    """A minimal HTTPMessage stub with an iter_body method."""

    def __init__(self, body: bytes):
        self._body = body

    def iter_body(self, chunk_size: int):
        """Yield the body in chunks of the given size."""
        for i in range(0, len(self._body), chunk_size):
            yield self._body[i : i + chunk_size]


def test_iter_body_chunks_normal():
    """RawStream should split the body into chunks of the requested size."""
    body = b"HelloWorld"
    msg = DummyMessage(body)
    stream = RawStream(chunk_size=5, msg=msg)
    chunks = list(stream.iter_body())
    assert chunks == [b"Hello", b"World"]
    assert all(isinstance(chunk, bytes) for chunk in chunks)


def test_iter_body_chunks_boundary():
    """If the chunk size exceeds the body length, the whole body is returned as one chunk."""
    body = b"Short"
    msg = DummyMessage(body)
    stream = RawStream(chunk_size=100, msg=msg)
    chunks = list(stream.iter_body())
    assert chunks == [b"Short"]
    assert len(chunks) == 1


def test_iter_body_returns_generator_and_bytes():
    """iter_body should return an iterable that yields bytes objects."""
    body = b"Data"
    msg = DummyMessage(body)
    stream = RawStream(chunk_size=2, msg=msg)
    result = stream.iter_body()
    assert hasattr(result, "__iter__")  # is iterable
    first_chunk = next(iter(result))
    assert isinstance(first_chunk, bytes)
    assert first_chunk == b"Da"
