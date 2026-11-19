import io
import zlib
import pytest
import requests
from httpie.uploads import compress_request


def test_compress_string_body_economical(tmp_path):
    # Create a small string that compresses well
    body = "a" * 1000
    req = requests.Request("POST", "http://example.com")
    prepped = req.prepare()
    prepped.body = body
    prepped.headers = {}

    compress_request(prepped, always=False)

    # Body should be compressed
    assert prepped.body is not None
    assert isinstance(prepped.body, bytes)
    # Content-Encoding header should be set
    assert prepped.headers.get("Content-Encoding") == "deflate"
    # Content-Length should match compressed size
    assert prepped.headers.get("Content-Length") == str(len(prepped.body))
    # Verify that decompression yields original body
    decompressed = zlib.decompress(prepped.body)
    assert decompressed.decode() == body


def test_compress_file_like_body_never_economical(tmp_path):
    # Create a file-like object that does not compress well
    data = b"".join([bytes([i % 256]) for i in range(1000)])
    file_obj = io.BytesIO(data)
    req = requests.Request("POST", "http://example.com")
    prepped = req.prepare()
    prepped.body = file_obj
    prepped.headers = {}

    compress_request(prepped, always=False)

    # Since compression is not economical, body should remain unchanged
    assert prepped.body == data
    # No Content-Encoding header should be added
    assert "Content-Encoding" not in prepped.headers
    # No Content-Length header should be added
    assert "Content-Length" not in prepped.headers


def test_compress_invalid_body_raises():
    req = requests.Request("POST", "http://example.com")
    prepped = req.prepare()
    prepped.body = None  # Invalid body type for compression
    prepped.headers = {}

    with pytest.raises(TypeError):
        compress_request(prepped, always=False)
