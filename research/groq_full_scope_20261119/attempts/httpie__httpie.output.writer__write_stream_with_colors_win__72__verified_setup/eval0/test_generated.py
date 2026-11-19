import io
import sys
import types
import pytest
from httpie.output.writer import write_stream_with_colors_win

class DummyStream:
    """Iterable that yields predefined byte chunks."""
    def __init__(self, chunks):
        self._chunks = chunks

    def __iter__(self):
        return iter(self._chunks)

class DummyTextIO:
    """TextIO-like object with a buffer and write/flush tracking."""
    def __init__(self, encoding='utf-8'):
        self.encoding = encoding
        self.buffer = io.BytesIO()
        self.written_text = []
        self.flushed = False

    def write(self, text):
        self.written_text.append(text)

    def flush(self):
        self.flushed = True

def test_write_stream_with_colors_win_basic_behavior(tmp_path):
    # Prepare a stream with a color chunk and non-color chunks
    chunks = [
        b'plain',
        b'\x1b[31mred\x1b[0m',
        b'plain2',
    ]
    stream = DummyStream(chunks)
    outfile = DummyTextIO(encoding='utf-8')

    write_stream_with_colors_win(stream, outfile, flush=False)

    # Non-color chunks should be written to the buffer
    assert outfile.buffer.getvalue() == b'plainplain2'
    # Color chunk should be decoded and written via write()
    assert outfile.written_text == ['red']
    # No flush should have occurred
    assert not outfile.flushed

def test_write_stream_with_colors_win_flush_behavior(tmp_path):
    # Stream with only color chunks
    chunks = [b'\x1b[32mgreen\x1b[0m']
    stream = DummyStream(chunks)
    outfile = DummyTextIO(encoding='utf-8')

    write_stream_with_colors_win(stream, outfile, flush=True)

    # Buffer should remain empty
    assert outfile.buffer.getvalue() == b''
    # Text written correctly
    assert outfile.written_text == ['green']
    # Flush should have been called
    assert outfile.flushed

def test_write_stream_with_colors_win_encoding_handling(tmp_path):
    # Stream with a color chunk that contains non-ASCII characters
    chunks = [b'\x1b[33m\xc3\xa9\x1b[0m']  # 'é' in UTF-8
    stream = DummyStream(chunks)
    outfile = DummyTextIO(encoding='utf-8')

    write_stream_with_colors_win(stream, outfile, flush=False)

    # The decoded text should be 'é'
    assert outfile.written_text == ['é']
    # No data should be in the buffer
    assert outfile.buffer.getvalue() == b''
