import io
import pytest
from httpie.output.writer import write_stream_with_colors_win
from httpie.output.streams import BaseStream


class DummyStream(BaseStream):
    """Simple BaseStream that yields predefined byte chunks."""
    def __init__(self, chunks):
        self._chunks = chunks

    def __iter__(self):
        return iter(self._chunks)


class DummyTextIO:
    """TextIO-like object with a buffer and encoding, tracking flush calls."""
    def __init__(self, encoding="utf-8"):
        self.buffer = io.BytesIO()
        self.encoding = encoding
        self.text = io.StringIO()
        self.flush_count = 0

    def write(self, s):
        """Write decoded string to the text buffer."""
        self.text.write(s)

    def flush(self):
        self.flush_count += 1


def test_write_stream_with_colors_win_writes_color_and_non_color_chunks(tmp_path):
    # Prepare chunks: one with ANSI color escape, one plain
    color_chunk = b"\x1b[31mred text\x1b[0m"
    plain_chunk = b"plain text"
    stream = DummyStream([color_chunk, plain_chunk])

    outfile = DummyTextIO()
    write_stream_with_colors_win(stream, outfile, flush=False)

    # Color chunk should be decoded and written to text buffer
    assert outfile.text.getvalue() == "red text"
    # Plain chunk should be written to binary buffer unchanged
    assert outfile.buffer.getvalue() == plain_chunk
    # No flush should have occurred
    assert outfile.flush_count == 0


def test_write_stream_with_colors_win_flushes_after_each_chunk(tmp_path):
    # Two chunks, flush enabled
    color_chunk = b"\x1b[32mgreen\x1b[0m"
    plain_chunk = b"data"
    stream = DummyStream([color_chunk, plain_chunk])

    outfile = DummyTextIO()
    write_stream_with_colors_win(stream, outfile, flush=True)

    # Text buffer contains decoded color text
    assert outfile.text.getvalue() == "green"
    # Binary buffer contains plain data
    assert outfile.buffer.getvalue() == plain_chunk
    # Flush should have been called twice (once per chunk)
    assert outfile.flush_count == 2


def test_write_stream_with_colors_win_handles_non_utf8_encoding(tmp_path):
    # Chunk with non-ASCII bytes that are not color escapes
    plain_chunk = b"\xff\xfe\xfd"
    stream = DummyStream([plain_chunk])

    # Use latin-1 encoding to avoid UnicodeDecodeError
    outfile = DummyTextIO(encoding="latin-1")
    write_stream_with_colors_win(stream, outfile, flush=False)

    # Since no color escape, bytes should go to buffer unchanged
    assert outfile.buffer.getvalue() == plain_chunk
    # Text buffer should remain empty
    assert outfile.text.getvalue() == ""
    # No flush
    assert outfile.flush_count == 0
