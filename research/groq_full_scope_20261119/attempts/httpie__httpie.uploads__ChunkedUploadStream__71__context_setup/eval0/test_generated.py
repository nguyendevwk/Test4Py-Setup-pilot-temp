import threading
import pytest
from httpie.uploads import ChunkedUploadStream, ChunkedStream

def test_chunked_upload_stream_iterates_and_calls_callback(tmp_path):
    # Prepare a simple iterable of bytes
    data = [b'hello', b'world']
    called_chunks = []

    def callback(chunk):
        called_chunks.append(chunk)

    stream = ChunkedUploadStream(data, callback)
    # Iterate over the stream and collect yielded chunks
    yielded = list(stream)
    assert yielded == data
    # Ensure callback was called with each chunk
    assert called_chunks == data

def test_chunked_upload_stream_sets_event_on_each_chunk(tmp_path):
    data = [b'chunk1', b'chunk2']
    event = threading.Event()
    called_chunks = []

    def callback(chunk):
        called_chunks.append(chunk)

    stream = ChunkedUploadStream(data, callback, event=event)
    # Initially the event should not be set
    assert not event.is_set()
    # Iterate over the stream
    list(stream)
    # After iteration, event should be set
    assert event.is_set()
    # Callback should have been called
    assert called_chunks == data

def test_chunked_upload_stream_with_empty_iterable(tmp_path):
    data = []
    called_chunks = []

    def callback(chunk):
        called_chunks.append(chunk)

    stream = ChunkedUploadStream(data, callback)
    yielded = list(stream)
    # No chunks should be yielded
    assert yielded == []
    # Callback should not be called
    assert called_chunks == []
