import io
import os
import pytest
from httpie.uploads import prepare_request_body, ChunkedUploadStream, ChunkedStream
from httpie.context import Environment
from httpie.cli.dicts import RequestDataDict

# Helper environment with minimal attributes used by _prepare_file_for_upload
class DummyEnv(Environment):
    def __init__(self):
        super().__init__()
        self.upload_chunk_size = 1024  # arbitrary chunk size

def test_prepare_request_body_with_bytes():
    env = DummyEnv()
    data = b"hello world"
    result = prepare_request_body(
        env=env,
        raw_body=data,
        body_read_callback=lambda x: None,
        offline=False,
        chunked=False,
    )
    assert isinstance(result, bytes)
    assert result == data

def test_prepare_request_body_with_file_like_offline():
    env = DummyEnv()
    file_content = b"file content"
    file_obj = io.BytesIO(file_content)
    result = prepare_request_body(
        env=env,
        raw_body=file_obj,
        body_read_callback=lambda x: None,
        offline=True,
        chunked=False,
    )
    assert isinstance(result, bytes)
    assert result == file_content

def test_prepare_request_body_with_file_like_chunked(tmp_path):
    env = DummyEnv()
    file_content = b"chunked data for upload"
    file_path = tmp_path / "test.txt"
    file_path.write_bytes(file_content)
    file_obj = open(file_path, "rb")
    result = prepare_request_body(
        env=env,
        raw_body=file_obj,
        body_read_callback=lambda x: None,
        offline=False,
        chunked=False,
    )
    assert isinstance(result, ChunkedStream)
    # Read all data from the returned stream
    read_data = b"".join(chunk for chunk in result)
    assert read_data == file_content
    file_obj.close()
