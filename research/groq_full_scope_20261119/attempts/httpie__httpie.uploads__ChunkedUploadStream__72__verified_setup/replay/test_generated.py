import threading
import pytest
from httpie.uploads import ChunkedUploadStream

def test_chunked_upload_stream_basic_iteration():
    # Prepare a simple iterable and a callback that records chunks
    data = [b'chunk1', b'chunk2', b'chunk3']
    recorded = []

    def callback(chunk):
        recorded.append(chunk)

    stream = ChunkedUploadStream(iter(data), callback)
    result = list(stream)

    # The stream should yield the same chunks as the original iterable
    assert result == data
    # The callback should have been called with each chunk
    assert recorded == data

def test_chunked_upload_stream_with_event():
    # Use an event to verify that it is set on each iteration
    data = [b'a', b'b', b'c']
    event = threading.Event()
    called_chunks = []

    def callback(chunk):
        called_chunks.append(chunk)

    stream = ChunkedUploadStream(iter(data), callback, event=event)
    # Before iteration, event should not be set
    assert not event.is_set()
    # Iterate over the stream
    list(stream)
    # After iteration, event should be set
    assert event.is_set()
    # Callback should have recorded all chunks
    assert called_chunks == data

def test_chunked_upload_stream_empty_iterable():
    # Test that an empty iterable yields nothing and callback is never called
    data = []
    called_chunks = []

    def callback(chunk):
        called_chunks.append(chunk)

    stream = ChunkedUploadStream(iter(data), callback)
    result = list(stream)

    assert result == []
    assert called_chunks == []
