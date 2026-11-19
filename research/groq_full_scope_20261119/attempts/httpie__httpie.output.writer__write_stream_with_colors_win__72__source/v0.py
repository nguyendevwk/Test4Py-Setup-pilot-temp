import io
import sys
import types
import pytest
from httpie.output.writer import write_stream_with_colors_win
from httpie.output.streams import BaseStream


class DummyStream(BaseStream):
    """A minimal BaseStream that yields predefined byte chunks."""
    def __init__(self, chunks):
        self._chunks = chunks

    def __iter__(self):
        return iter(self._chunks)


class RecordingTextIO(io.TextIOBase):
    """TextIO that records flush calls and delegates to an underlying BytesIO buffer."""
    def __init__(self, encoding="utf-8"):
        self._buffer = io.BytesIO()
        self.encoding = encoding
        self.flush_called = False

    @property
    def buffer(self):
        return self._buffer

    def write(self, s):
        # TextIOBase.write expects str; encode to bytes
        return self._buffer.write(s.encode(self.encoding))

    def flush(self):
        self.flush_called = True
        # No-op for underlying buffer


def test_write_stream_with_colors_win_decodes_color_sequences(tmp_path):
    """Chunks containing ANSI escape codes are decoded to text."""
    # Prepare a stream with a color escape sequence and a normal chunk
    color_escape = b'\x1b[31m'  # red
    normal = b'Hello'
    stream = DummyStream([color_escape + normal, b'World'])
    outfile = RecordingTextIO()
    write_stream_with_colors_win(stream, outfile, flush=False)

    # The buffer should contain the raw bytes for the normal chunk
    assert outfile.buffer.getvalue() == b'World'
    # The decoded text should be written to the text buffer
    outfile.buffer.seek(0)
    assert outfile.buffer.read() == b'World'  # only raw bytes written
    # The decoded part should have been written via TextIOBase.write
    # Since we used RecordingTextIO, the buffer contains the decoded text
    # in the underlying BytesIO; we check that the decoded part is present
    # by reading from the buffer after the first write
    outfile.buffer.seek(0)
    decoded_part = outfile.buffer.read(len(color_escape) + len(normal))
    assert decoded_part == color_escape + normal


def test_write_stream_with_colors_win_flush_behavior(tmp_path):
    """When flush=True, the outfile.flush method is called after each chunk."""
    stream = DummyStream([b'chunk1', b'chunk2'])
    outfile = RecordingTextIO()
    write_stream_with_colors_win(stream, outfile, flush=True)

    # flush should have been called at least once
    assert outfile.flush_called is True
    # The buffer should contain all raw chunks
    assert outfile.buffer.getvalue() == b'chunk1chunk2'


def test_write_stream_with_colors_win_handles_mixed_chunks(tmp_path):
    """Stream with alternating color and non-color chunks is processed correctly."""
    color = b'\x1b[32m'  # green
    stream = DummyStream([color + b'Green', b'Plain', color + b'MoreGreen'])
    outfile = RecordingTextIO()
    write_stream_with_colors_win(stream, outfile, flush=False)

    # Raw buffer should contain only the plain chunk
    assert outfile.buffer.getvalue() == b'Plain'
    # The decoded text should be written to the text buffer
    # Since we used RecordingTextIO, the buffer contains the decoded text
    # in the underlying BytesIO; we check that the decoded parts are present
    outfile.buffer.seek(0)
    decoded = outfile.buffer.read()
    # The decoded text should include the color escapes and the words
    assert decoded == color + b'Green' + color + b'MoreGreen'
