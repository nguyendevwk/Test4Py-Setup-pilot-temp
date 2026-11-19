import io
import os
import threading
import pytest
from httpie.uploads import prepare_request_body, ChunkedUploadStream
from httpie.context import Environment
from httpie.cli.dicts import RequestDataDict

def test_prepare_request_body_with_bytes_and_callback(tmp_path):
    env = Environment()
    body = b"hello world"
    callback_called = threading.Event()
    def callback(chunk):
        assert chunk == body
        callback_called.set()
    result = prepare_request_body(env, body, callback, offline=False, chunked=False)
    assert result == body
    assert callback_called.is_set()

def test_prepare_request_body_with_file_like_and_callback(tmp_path):
    env = Environment()
    file_path = tmp_path / "test.txt"
    file_path.write_bytes(b"file content")
    file_obj = open(file_path, "rb")
    callback_called = threading.Event()
    def callback(chunk):
        assert isinstance(chunk, bytes)
        callback_called.set()
    result = prepare_request_body(env, file_obj, callback, offline=False, chunked=False)
    assert isinstance(result, io.BufferedReader)
    # Read to trigger callback
    data = result.read()
    assert data == b"file content"
    assert callback_called.is_set()
    file_obj.close()

def test_prepare_request_body_with_chunked_stream(tmp_path):
    env = Environment()
    body = b"chunked data"
    callback_called = threading.Event()
    def callback(chunk):
        assert chunk == body
        callback_called.set()
    result = prepare_request_body(env, body, callback, offline=False, chunked=True)
    assert isinstance(result, ChunkedUploadStream)
    chunks = list(result)
    assert chunks == [body]
    assert callback_called.is_set()
