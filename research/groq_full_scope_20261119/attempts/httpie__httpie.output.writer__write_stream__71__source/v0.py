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


class FlushTracker(io.BytesIO):
    """BytesIO that records whether flush was called."""
    def __init__(self):
        super().__init__()
        self.flushed = False

    def flush(self):
        self.flushed = True
        super().flush()


def test_write_stream_with_flush_and_no_buffer(tmp_path):
    """write_stream writes chunks to a BytesIO and flushes when requested."""
    data = [b"hello ", b"world"]
    stream = DummyStream(data)
    outfile = FlushTracker()

    write_stream(stream, outfile, flush=True)

    # The buffer should contain the concatenated data
    assert outfile.getvalue() == b"hello world"
    # Flush should have been called after each chunk
    assert outfile.flushed is True


def test_write_stream_with_buffer(tmp_path):
    """write_stream writes to the buffer attribute of a TextIOWrapper."""
    data = [b"foo", b"bar"]
    stream = DummyStream(data)
    # Create a TextIOWrapper around a BytesIO to provide a .buffer attribute
    raw = io.BytesIO()
    outfile = io.TextIOWrapper(raw, encoding="utf-8")

    write_stream(stream, outfile, flush=False)

    # The underlying buffer should contain the raw bytes
    assert raw.getvalue() == b"foobar"
    # Since flush=False, the TextIOWrapper should not have flushed the buffer
    # (TextIOWrapper flushes its own buffer, but we can check that raw buffer is unchanged)
    assert outfile.tell() == 0  # no characters written to the TextIOWrapper


def test_write_stream_propagates_stream_exception():
    """write_stream should propagate exceptions raised by the stream iterator."""
    class ErrorStream(BaseStream):
        def __iter__(self):
            raise RuntimeError("stream error")

    stream = ErrorStream()
    outfile = io.BytesIO()

    with pytest.raises(RuntimeError, match="stream error"):
        write_stream(stream, outfile, flush=False)
