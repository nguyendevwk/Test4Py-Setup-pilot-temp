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


class FlushTrackingBytesIO(io.BytesIO):
    """BytesIO that tracks flush calls."""
    def __init__(self):
        super().__init__()
        self.flush_called = False

    def flush(self):
        self.flush_called = True
        super().flush()


def test_write_stream_writes_chunks_to_buffered_output(tmp_path):
    """write_stream should write all chunks to the outfile.buffer when available."""
    # Create a TextIOWrapper over a BytesIO to provide a buffer attribute
    raw = io.BytesIO()
    text_wrapper = io.TextIOWrapper(raw, encoding="utf-8")
    stream = DummyStream([b"hello ", b"world"])
    write_stream(stream, text_wrapper, flush=False)
    # The underlying buffer should contain the concatenated bytes
    assert raw.getvalue() == b"hello world"
    # No flush should have been called
    assert not text_wrapper.flush_called  # TextIOWrapper has no flush_called attribute


def test_write_stream_flushes_when_requested(tmp_path):
    """write_stream should call flush on the outfile when flush=True."""
    outfile = FlushTrackingBytesIO()
    stream = DummyStream([b"foo", b"bar"])
    write_stream(stream, outfile, flush=True)
    assert outfile.getvalue() == b"foobar"
    assert outfile.flush_called, "flush should have been called when flush=True"


def test_write_stream_propagates_stream_exceptions():
    """write_stream should propagate exceptions raised by the stream iterator."""
    def bad_generator():
        yield b"good"
        raise RuntimeError("stream error")

    stream = DummyStream(bad_generator())
    outfile = io.BytesIO()
    with pytest.raises(RuntimeError, match="stream error"):
        write_stream(stream, outfile, flush=False)
    # Ensure that the first chunk was written before the exception
    assert outfile.getvalue() == b"good"
