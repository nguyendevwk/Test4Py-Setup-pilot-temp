import io
import pytest
from httpie.output.writer import write_stream_with_colors_win
from httpie.output.streams import BaseStream


class DummyStream(BaseStream):
    """A minimal BaseStream that yields predefined byte chunks."""
    def __init__(self, chunks):
        self._chunks = chunks

    def __iter__(self):
        return iter(self._chunks)


class TextIOWithBuffer(io.TextIOBase):
    """TextIO that exposes a buffer and records flush calls."""
    def __init__(self, encoding="utf-8"):
        super().__init__()
        self._buffer = io.BytesIO()
        self.encoding = encoding
        self.flush_calls = 0
        self._text = io.StringIO()

    @property
    def buffer(self):
        return self._buffer

    def write(self, s):
        """Write decoded text to the internal StringIO."""
        self._text.write(s)

    def flush(self):
        self.flush_calls += 1

    def getvalue(self):
        return self._text.getvalue()

    def getbuffer(self):
        return self._buffer.getvalue()


def test_write_stream_with_colors_win_decodes_color_chunks(tmp_path):
    # Prepare chunks: one with ANSI color code, one without
    color_chunk = b"\x1b[31mRed Text\x1b[0m"
    plain_chunk = b"Plain text"
    stream = DummyStream([color_chunk, plain_chunk])

    outfile = TextIOWithBuffer(encoding="utf-8")
    write_stream_with_colors_win(stream, outfile, flush=False)

    # Color chunk should be decoded and written to text
    assert outfile.getvalue() == "Red Text"
    # Plain chunk should be written to the buffer unchanged
    assert outfile.getbuffer() == plain_chunk
    # No flush should have occurred
    assert outfile.flush_calls == 0


def test_write_stream_with_colors_win_flushes_output(tmp_path):
    # Two chunks, both plain, to test flush behavior
    chunk1 = b"First"
    chunk2 = b"Second"
    stream = DummyStream([chunk1, chunk2])

    outfile = TextIOWithBuffer(encoding="utf-8")
    write_stream_with_colors_win(stream, outfile, flush=True)

    # All data should be in buffer
    assert outfile.getbuffer() == chunk1 + chunk2
    # No text written
    assert outfile.getvalue() == ""
    # Flush should have been called twice (once per chunk)
    assert outfile.flush_calls == 2


def test_write_stream_with_colors_win_handles_mixed_chunks(tmp_path):
    # Mixed color and plain chunks, with flush disabled
    color_chunk = b"\x1b[32mGreen\x1b[0m"
    plain_chunk = b"Text"
    stream = DummyStream([color_chunk, plain_chunk, color_chunk])

    outfile = TextIOWithBuffer(encoding="utf-8")
    write_stream_with_colors_win(stream, outfile, flush=False)

    # Text should contain decoded color chunks concatenated
    assert outfile.getvalue() == "GreenGreen"
    # Buffer should contain the plain chunk only
    assert outfile.getbuffer() == plain_chunk
    # No flush calls
    assert outfile.flush_calls == 0
