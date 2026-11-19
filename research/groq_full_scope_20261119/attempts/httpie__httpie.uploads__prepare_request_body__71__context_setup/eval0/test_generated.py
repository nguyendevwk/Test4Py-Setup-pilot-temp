import io
import sys
import threading
import types
import pytest
from httpie.uploads import (
    prepare_request_body,
    ChunkedUploadStream,
    _prepare_file_for_upload,
    as_bytes,
)
from httpie.cli.dicts import RequestDataDict
from httpie.context import Environment


class DummyEnv(Environment):
    def __init__(self):
        super().__init__()
        self.stderr = io.StringIO()


def test_prepare_request_body_with_file_and_callback(tmp_path: pytest.TempPathFactory):
    env = DummyEnv()
    # Create a temporary file with known content
    file_path = tmp_path / "test.txt"
    file_path.write_text("hello world")
    file_obj = open(file_path, "rb")

    callback_calls = []

    def callback(chunk):
        callback_calls.append(chunk)

    # Prepare body with a file-like object
    result = prepare_request_body(
        env=env,
        raw_body=file_obj,
        body_read_callback=callback,
        offline=False,
        chunked=False,
    )

    # The result should be the same file object with its read method wrapped
    assert result is file_obj
    # Read the file to trigger callback
    data = result.read()
    assert data == b"hello world"
    # Callback should have been called once with the read chunk
    assert callback_calls == [b"hello world"]
    file_obj.close()


def test_prepare_request_body_chunked_stream_and_callback():
    env = DummyEnv()
    data = b"chunked data test"
    callback_calls = []

    def callback(chunk):
        callback_calls.append(chunk)

    # Prepare body as a string with chunked=True
    result = prepare_request_body(
        env=env,
        raw_body=data,
        body_read_callback=callback,
        offline=False,
        chunked=True,
    )

    # Result should be a ChunkedUploadStream
    assert isinstance(result, ChunkedUploadStream)

    # Iterate over the stream and collect chunks
    collected = list(result)
    assert collected == [data]
    # Callback should have been called once with the chunk
    assert callback_calls == [data]


def test_prepare_request_body_offline_and_requestdatadict():
    env = DummyEnv()
    # Create a RequestDataDict
    rdd = RequestDataDict({"a": "1", "b": ["2", "3"]})
    # Prepare body with offline=True
    result = prepare_request_body(
        env=env,
        raw_body=rdd,
        body_read_callback=lambda x: x,
        offline=True,
        chunked=False,
    )
    # In offline mode, the body should be returned as bytes
    assert isinstance(result, bytes)
    # The bytes should be the URL-encoded representation
    assert result == b"a=1&b=2&b=3"
