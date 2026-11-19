import io
import os
import pytest
from httpie.output.writer import write_stream
from httpie.output.streams import BaseStream


class DummyStream(BaseStream):
    """A minimal BaseStream that yields the provided chunks."""
    def __init__(self, chunks):
        self._chunks = chunks

    def __iter__(self):
        return iter(self._chunks)


def test_write_stream_to_file(tmp_path):
    """Normal case: write bytes to a binary file and verify content."""
    file_path = tmp_path / "output.bin"
    stream = DummyStream([b"hello ", b"world"])
    with open(file_path, "wb") as f:
        write_stream(stream, f, flush=True)
    assert file_path.read_bytes() == b"hello world"


def test_write_stream_to_textio():
    """Boundary case: writing to a TextIO that has no buffer attribute."""
    stream = DummyStream([b"foo", b"bar"])
    text_io = io.StringIO()
    # The function should fall back to using the TextIO directly.
    # Writing bytes to a StringIO will raise a TypeError.
    with pytest.raises(TypeError):
        write_stream(stream, text_io, flush=False)


def test_write_stream_with_invalid_chunk():
    """Error case: stream yields a non-bytes chunk causing a write error."""
    stream = DummyStream([b"valid", "invalid_chunk"])
    buf = io.BytesIO()
    with pytest.raises(TypeError):
        write_stream(stream, buf, flush=False)
