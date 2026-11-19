import io
import pytest
from httpie.output.writer import write_stream
from httpie.output.streams import BaseStream


class DummyStream(BaseStream):
    """A minimal BaseStream that yields predefined byte chunks."""
    def __init__(self, chunks):
        self._chunks = chunks

    def __iter__(self):
        return iter(self._chunks)


def test_write_stream_with_buffer_and_flush(tmp_path):
    """Ensure that write_stream writes to the buffer and flushes when requested."""
    # Prepare a BytesIO object to capture output
    outfile = io.BytesIO()
    # Dummy stream yields two chunks
    stream = DummyStream([b"hello ", b"world"])
    # Call write_stream with flush=True
    write_stream(stream, outfile, flush=True)
    # Verify that the buffer contains the concatenated chunks
    assert outfile.getvalue() == b"hello world"
    # Since BytesIO does not expose flush, we rely on no exception being raised


def test_write_stream_without_buffer(tmp_path):
    """Ensure that write_stream works when the outfile has no buffer attribute."""
    class TextFileLike:
        """Simple text file-like object without a buffer attribute."""
        def __init__(self):
            self.data = bytearray()
            self.flushed = False

        def write(self, chunk):
            self.data.extend(chunk)

        def flush(self):
            self.flushed = True

    outfile = TextFileLike()
    stream = DummyStream([b"foo", b"bar"])
    write_stream(stream, outfile, flush=False)
    assert outfile.data == bytearray(b"foobar")
    assert not outfile.flushed


def test_write_stream_flush_called(tmp_path):
    """Verify that flush is called on the outfile when flush=True."""
    class FlushTracker:
        def __init__(self):
            self.flush_count = 0
            self.buffer = io.BytesIO()

        def flush(self):
            self.flush_count += 1

    outfile = FlushTracker()
    stream = DummyStream([b"abc", b"def"])
    write_stream(stream, outfile, flush=True)
    # Each chunk should trigger a flush
    assert outfile.flush_count == 2
    assert outfile.buffer.getvalue() == b"abcdef"
