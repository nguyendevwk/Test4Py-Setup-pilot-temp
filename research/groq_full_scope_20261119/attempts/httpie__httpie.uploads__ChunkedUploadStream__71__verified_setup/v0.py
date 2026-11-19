import threading
import pytest
from httpie.uploads import ChunkedUploadStream


def test_chunked_upload_stream_normal_iteration(tmp_path):
    # Prepare a simple iterable of bytes
    data = [b'chunk1', b'chunk2', b'chunk3']
    callback_calls = []

    def callback(chunk):
        callback_calls.append(chunk)

    event = threading.Event()
    stream = ChunkedUploadStream(data, callback, event)

    # Iterate over the stream and collect yielded chunks
    yielded = list(stream)

    # Assertions
    assert yielded == data, "Yielded chunks should match the input data"
    assert callback_calls == data, "Callback should be called with each chunk"
    assert event.is_set(), "Event should be set after iteration starts"


def test_chunked_upload_stream_empty_iterable(tmp_path):
    # Empty iterable
    data = []
    callback_calls = []

    def callback(chunk):
        callback_calls.append(chunk)

    event = threading.Event()
    stream = ChunkedUploadStream(data, callback, event)

    yielded = list(stream)

    # Assertions
    assert yielded == [], "Yielded list should be empty for empty input"
    assert callback_calls == [], "Callback should not be called for empty input"
    assert not event.is_set(), "Event should not be set when no chunks are processed"


def test_chunked_upload_stream_callback_exception(tmp_path):
    # Iterable with one chunk
    data = [b'error_chunk']
    callback_calls = []

    def callback(chunk):
        callback_calls.append(chunk)
        raise ValueError("callback error")

    event = threading.Event()
    stream = ChunkedUploadStream(data, callback, event)

    with pytest.raises(ValueError, match="callback error"):
        list(stream)

    # Assertions after exception
    assert callback_calls == [b'error_chunk'], "Callback should be called once before exception"
    assert event.is_set(), "Event should be set even if callback raises an exception"
