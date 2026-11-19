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


class FlushCounterBytesIO(io.BytesIO):
    """BytesIO that counts how many times flush() is called."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flush_calls = 0

    def flush(self):
        self.flush_calls += 1
        super().flush()


def test_write_stream_writes_bytes_to_buffer(tmp_path):
    """write_stream should write all chunks to a binary buffer."""
    # Prepare a stream that yields three byte chunks
    chunks = [b'hello', b' ', b'world']
    stream = DummyStream(chunks)

    # Use a BytesIO as the output file
    outfile = io.BytesIO()

    # Call write_stream without flushing
    write_stream(stream, outfile, flush=False)

    # The buffer should contain the concatenated chunks
    outfile.seek(0)
    assert outfile.read() == b'hello world'


def test_write_stream_flushes_when_requested(tmp_path):
    """write_stream should call flush on the output file when flush=True."""
    # Prepare a stream that yields a single byte chunk
    stream = DummyStream([b'abc'])

    # Use a custom BytesIO that counts flush calls
    outfile = FlushCounterBytesIO()

    # Call write_stream with flush=True
    write_stream(stream, outfile, flush=True)

    # The buffer should contain the chunk
    outfile.seek(0)
    assert outfile.read() == b'abc'

    # flush() should have been called exactly once
    assert outfile.flush_calls == 1


def test_write_stream_raises_on_text_stream(tmp_path):
    """write_stream should raise a TypeError when given a text stream that cannot accept bytes."""
    # Prepare a stream that yields a single byte chunk
    stream = DummyStream([b'xyz'])

    # Use a StringIO which expects str, not bytes
    outfile = io.StringIO()

    # write_stream should raise a TypeError because StringIO.write expects str
    with pytest.raises(TypeError):
        write_stream(stream, outfile, flush=False)
