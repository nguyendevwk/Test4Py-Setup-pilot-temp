import io
import sys
import types
import pytest
from httpie.output.writer import write_stream, write_stream_with_colors_win, BaseStream

# --------------------------------------------------------------------------- #
# Helper stream that yields a predefined sequence of byte chunks
class DummyStream(BaseStream):
    def __init__(self, chunks):
        self._chunks = chunks

    def __iter__(self):
        return iter(self._chunks)

# --------------------------------------------------------------------------- #
# Test that write_stream writes all chunks to the buffer and flushes when
# requested.
def test_write_stream_bytes_and_flush(tmp_path):
    # Prepare a BytesIO buffer and a dummy outfile that forwards writes to it
    buffer = io.BytesIO()
    class DummyFile:
        def __init__(self, buf):
            self.buffer = buf
        def flush(self):
            # No-op flush for BytesIO
            pass
    outfile = DummyFile(buffer)

    # Dummy stream yielding two chunks
    stream = DummyStream([b'hello', b'world'])

    # Write without flushing
    write_stream(stream, outfile, flush=False)
    assert buffer.getvalue() == b'helloworld'

    # Reset buffer and write with flushing
    buffer.seek(0)
    buffer.truncate(0)
    write_stream(stream, outfile, flush=True)
    assert buffer.getvalue() == b'helloworld'

# --------------------------------------------------------------------------- #
# Test that write_stream_with_colors_win writes color chunks as text and
# non‑color chunks as bytes, and flushes when requested.
def test_write_stream_with_colors_win(tmp_path):
    # Create a BytesIO underlying buffer and a TextIOWrapper over it
    underlying = io.BytesIO()
    outfile = io.TextIOWrapper(underlying, encoding='utf-8')

    # Dummy stream yielding a color chunk and a non‑color chunk
    color_chunk = b'\x1b[31mred text\x1b[0m'
    non_color_chunk = b'plain text'
    stream = DummyStream([color_chunk, non_color_chunk])

    # Capture writes to the underlying buffer and to the text stream
    original_write = outfile.write
    writes = []

    def capture_write(s):
        writes.append(('text', s))
        return original_write(s)

    outfile.write = capture_write

    # Capture buffer writes
    original_buffer_write = underlying.write
    buffer_writes = []

    def capture_buffer_write(b):
        buffer_writes.append(b)
        return original_buffer_write(b)

    underlying.write = capture_buffer_write

    # Perform the write with flushing
    write_stream_with_colors_win(stream, outfile, flush=True)

    # Verify that the color chunk was written as text
    assert writes == [('text', 'red text')]
    # Verify that the non‑color chunk was written to the buffer
    assert buffer_writes == [b'plain text']
    # Verify that the underlying buffer contains the non‑color chunk
    assert underlying.getvalue() == b'plain text'

# --------------------------------------------------------------------------- #
# Test that write_stream does not raise an exception when the output file
# is a simple BytesIO and flush is False.
def test_write_stream_no_exception(tmp_path):
    buffer = io.BytesIO()
    class DummyFile:
        def __init__(self, buf):
            self.buffer = buf
        def flush(self):
            pass
    outfile = DummyFile(buffer)
    stream = DummyStream([b'test'])
    # Should not raise
    write_stream(stream, outfile, flush=False)
    assert buffer.getvalue() == b'test'
