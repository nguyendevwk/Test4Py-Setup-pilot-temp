import pytest
from httpie.output.streams import RawStream
from httpie.models import HTTPMessage, OutputOptions
from httpie.context import Environment

def test_rawstream_iter_body_chunks_exact():
    # Create a message with body exactly 3 * 10 bytes
    body = b"0123456789" * 3  # 30 bytes
    msg = HTTPMessage(body=body, headers={}, status=200, method="GET", url="http://example.com")
    stream = RawStream(msg=msg, env=Environment(), options=OutputOptions())
    # Use a small chunk size to force multiple chunks
    stream.chunk_size = 10
    chunks = list(stream.iter_body())
    assert chunks == [body[i:i+10] for i in range(0, len(body), 10)]
    assert all(isinstance(chunk, bytes) for chunk in chunks)

def test_rawstream_iter_body_chunk_size_larger_than_body():
    # Body smaller than chunk size
    body = b"short"
    msg = HTTPMessage(body=body, headers={}, status=200, method="GET", url="http://example.com")
    stream = RawStream(msg=msg, env=Environment(), options=OutputOptions())
    stream.chunk_size = 1024  # larger than body
    chunks = list(stream.iter_body())
    assert chunks == [body]
    assert len(chunks) == 1

def test_rawstream_iter_body_invalid_chunk_size():
    # Passing zero or negative chunk size should raise ValueError
    body = b"data"
    msg = HTTPMessage(body=body, headers={}, status=200, method="GET", url="http://example.com")
    stream = RawStream(msg=msg, env=Environment(), options=OutputOptions())
    with pytest.raises(ValueError):
        stream.chunk_size = 0
    with pytest.raises(ValueError):
        stream.chunk_size = -5
