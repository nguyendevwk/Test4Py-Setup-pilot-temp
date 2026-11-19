import threading
import pytest
from httpie.uploads import ChunkedUploadStream


def test_chunked_upload_stream_calls_callback_and_sets_event(tmp_path):
    # Prepare a simple stream of bytes
    stream = [b"chunk1", b"chunk2", b"chunk3"]
    called_chunks = []

    def callback(chunk):
        called_chunks.append(chunk)

    event = threading.Event()
    stream_obj = ChunkedUploadStream(stream, callback, event)

    # Iterate over the stream and collect yielded chunks
    yielded = list(stream_obj)

    # Assertions
    assert yielded == stream, "Yielded chunks should match the original stream"
    assert called_chunks == stream, "Callback should be called with each chunk"
    assert event.is_set(), "Event should be set after iteration"


def test_chunked_upload_stream_without_event(tmp_path):
    # Stream with a single chunk
    stream = [b"only_chunk"]
    called_chunks = []

    def callback(chunk):
        called_chunks.append(chunk)

    # No event passed
    stream_obj = ChunkedUploadStream(stream, callback)

    yielded = list(stream_obj)

    assert yielded == stream, "Yielded chunks should match the original stream"
    assert called_chunks == stream, "Callback should be called with the chunk"
    # No event to check, just ensure no exception was raised


def test_chunked_upload_stream_callback_side_effects(tmp_path):
    # Stream with two chunks
    stream = [b"first", b"second"]
    collected = []

    def callback(chunk):
        # Append the length of the chunk to collected list
        collected.append(len(chunk))

    event = threading.Event()
    stream_obj = ChunkedUploadStream(stream, callback, event)

    yielded = list(stream_obj)

    assert yielded == stream, "Yielded chunks should match the original stream"
    assert collected == [5, 6], "Callback should record lengths of chunks"
    assert event.is_set(), "Event should be set after iteration"
