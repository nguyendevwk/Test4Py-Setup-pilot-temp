import threading
import pytest
from httpie.uploads import ChunkedUploadStream

def test_chunked_upload_stream_iterates_and_calls_callback():
    # Prepare a stream of bytes and a callback that records chunks
    stream = [b'chunk1', b'chunk2', b'chunk3']
    called_chunks = []

    def callback(chunk):
        called_chunks.append(chunk)

    upload_stream = ChunkedUploadStream(stream, callback)
    result_chunks = list(upload_stream)

    # The iterator should yield the same chunks as the original stream
    assert result_chunks == stream
    # The callback should have been called with each chunk in order
    assert called_chunks == stream

def test_chunked_upload_stream_sets_event_for_each_chunk():
    # Prepare a stream and an event
    stream = [b'one', b'two']
    event = threading.Event()
    called_chunks = []

    def callback(chunk):
        called_chunks.append(chunk)

    upload_stream = ChunkedUploadStream(stream, callback, event=event)

    # The event should not be set before iteration
    assert not event.is_set()

    # Iterate over the stream
    list(upload_stream)

    # After iteration, the event should be set
    assert event.is_set()
    # Callback should have been called for each chunk
    assert called_chunks == stream

def test_chunked_upload_stream_propagates_callback_exception():
    # Prepare a stream and a callback that raises an exception on a specific chunk
    stream = [b'first', b'bad', b'last']
    called_chunks = []

    def callback(chunk):
        called_chunks.append(chunk)
        if chunk == b'bad':
            raise ValueError("callback error")

    upload_stream = ChunkedUploadStream(stream, callback)

    # Iteration should raise the exception from the callback
    with pytest.raises(ValueError, match="callback error"):
        list(upload_stream)

    # The callback should have been called for the first chunk before the error
    assert called_chunks == [b'first']
