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


class FlushCounter(io.BytesIO):
    """BytesIO that counts flush calls."""
    def __init__(self):
        super().__init__()
        self.flush_calls = 0

    def flush(self):
        self.flush_calls += 1
        super().flush()


def test_write_stream_with_buffer_and_flush():
    """When the outfile has a buffer attribute, data is written to it and flush is called."""
    stream = DummyStream([b'hello', b' ', b'world'])
    outfile = FlushCounter()
    write_stream(stream, outfile, flush=True)
    # The buffer of BytesIO is the BytesIO itself
    assert outfile.getvalue() == b'hello world'
    # flush should have been called after each chunk (3 times)
    assert outfile.flush_calls == 3


def test_write_stream_without_buffer():
    """When the outfile lacks a buffer attribute, write_stream writes directly to it."""
    class SimpleWriter:
        def __init__(self):
            self.data = bytearray()
            self.flushed = False

        def write(self, chunk):
            self.data.extend(chunk)

        def flush(self):
            self.flushed = True

    stream = DummyStream([b'foo', b'bar'])
    writer = SimpleWriter()
    write_stream(stream, writer, flush=False)
    assert writer.data == b'foobar'
    assert not writer.flushed


def test_write_stream_flush_flag_false():
    """When flush flag is False, outfile.flush() is never called."""
    stream = DummyStream([b'abc', b'def'])
    outfile = FlushCounter()
    write_stream(stream, outfile, flush=False)
    assert outfile.getvalue() == b'abcdef'
    assert outfile.flush_calls == 0
