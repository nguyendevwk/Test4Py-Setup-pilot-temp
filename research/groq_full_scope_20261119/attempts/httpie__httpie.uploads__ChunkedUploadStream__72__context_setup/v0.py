import threading
import pytest
from httpie.uploads import ChunkedUploadStream, ChunkedStream


def test_chunked_upload_stream_yields_chunks_and_calls_callback():
    # Prepare a stream of chunks and a callback that records calls
    chunks = [b"first", b"second", b"third"]
    called_chunks = []

    def callback(chunk):
        called_chunks.append(chunk)

    stream = ChunkedUploadStream(iter(chunks), callback)
    # Iterate over the stream and collect the yielded chunks
    yielded = list(stream)

    # The yielded chunks should match the original chunks
    assert yielded == chunks
    # The callback should have been called with each chunk
    assert called_chunks == chunks


def test_chunked_upload_stream_sets_event_on_each_iteration():
    # Prepare a stream and an event
    chunks = [b"chunk1", b"chunk2"]
    event = threading.Event()
    # Callback that does nothing
    def callback(chunk):
        pass

    stream = ChunkedUploadStream(iter(chunks), callback, event=event)

    # Before iteration, the event should not be set
    assert not event.is_set()

    # Iterate once; the event should be set after the first chunk
    iterator = iter(stream)
    next(iterator)
    assert event.is_set()

    # Reset the event for the next chunk
    event.clear()
    next(iterator)
    assert event.is_set()


def test_chunked_upload_stream_without_event_does_not_raise():
    # Prepare a stream and a callback that records calls
    chunks = [b"a", b"b"]
    called_chunks = []

    def callback(chunk):
        called_chunks.append(chunk)

    # Create stream without providing an event
    stream = ChunkedUploadStream(iter(chunks), callback)

    # Iterating should not raise any exception
    yielded = list(stream)

    # Verify that the yielded chunks and callback calls are correct
    assert yielded == chunks
    assert called_chunks == chunks
