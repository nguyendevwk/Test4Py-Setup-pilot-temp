import io
import zlib
import requests
import pytest
from httpie.uploads import compress_request


def test_compress_string_body_economical(tmp_path):
    # Create a small string that compresses well
    body = "a" * 1000  # repeated char compresses significantly
    req = requests.Request("POST", "http://example.com", data=body).prepare()
    compress_request(req, always=False)
    # Body should be compressed
    assert req.body is not None
    assert isinstance(req.body, bytes)
    # Content-Encoding header should be set
    assert req.headers.get("Content-Encoding") == "deflate"
    # Length header should match compressed body length
    assert int(req.headers["Content-Length"]) == len(req.body)
    # Verify that decompression yields original body
    decompressed = zlib.decompress(req.body)
    assert decompressed.decode() == body


def test_compress_file_like_body_non_economical_always(tmp_path):
    # Create a file-like object with data that does not compress well
    data = b"".join([bytes([i % 256]) for i in range(1000)])  # random-ish data
    file_obj = io.BytesIO(data)
    req = requests.Request("POST", "http://example.com", data=file_obj).prepare()
    # Ensure body is read from file-like object
    assert isinstance(req.body, bytes)
    # Compress with always=True to force compression even if not economical
    compress_request(req, always=True)
    # Body should still be compressed
    assert isinstance(req.body, bytes)
    assert req.headers.get("Content-Encoding") == "deflate"
    # Length header should match compressed body length
    assert int(req.headers["Content-Length"]) == len(req.body)
    # Decompress to verify integrity
    decompressed = zlib.decompress(req.body)
    assert decompressed == data


def test_compress_none_body_no_change(tmp_path):
    # Prepare a request with no body
    req = requests.Request("GET", "http://example.com").prepare()
    # Body is None
    assert req.body is None
    # Compress should leave body unchanged
    compress_request(req, always=False)
    assert req.body is None
    # No Content-Encoding header should be added
    assert "Content-Encoding" not in req.headers
    assert "Content-Length" not in req.headers
