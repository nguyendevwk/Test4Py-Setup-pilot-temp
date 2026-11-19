import io
import zlib
import requests
import pytest
from httpie.uploads import compress_request

def test_compress_request_with_string_body(tmp_path):
    # Prepare a request with a string body that will be compressed
    body = "Hello, world! " * 10  # repeat to make compression effective
    req = requests.Request("POST", "http://example.com", data=body)
    prepped = req.prepare()
    compress_request(prepped, always=False)

    # Body should now be compressed bytes
    assert isinstance(prepped.body, bytes)
    # Content-Encoding header should be set
    assert prepped.headers["Content-Encoding"] == "deflate"
    # Content-Length should match compressed size
    assert prepped.headers["Content-Length"] == str(len(prepped.body))
    # Decompress to verify integrity
    decompressed = zlib.decompress(prepped.body)
    assert decompressed.decode() == body

def test_compress_request_with_file_like_body(tmp_path):
    # Create a temporary file with content that compresses well
    file_path = tmp_path / "test.txt"
    file_path.write_text("A" * 1000)  # repetitive content
    with open(file_path, "rb") as f:
        req = requests.Request("POST", "http://example.com", data=f)
        prepped = req.prepare()
        compress_request(prepped, always=False)

        # Body should be compressed bytes
        assert isinstance(prepped.body, bytes)
        # Content-Encoding header should be set
        assert prepped.headers["Content-Encoding"] == "deflate"
        # Content-Length should match compressed size
        assert prepped.headers["Content-Length"] == str(len(prepped.body))
        # Decompress to verify integrity
        decompressed = zlib.decompress(prepped.body)
        assert decompressed == b"A" * 1000

def test_compress_request_when_not_economical_and_always_true(tmp_path):
    # Prepare a request with a body that does not compress well
    body = b"Unique data that won't compress much" * 1
    req = requests.Request("POST", "http://example.com", data=body)
    prepped = req.prepare()
    # Ensure compression is not economical
    deflater = zlib.compressobj()
    compressed = deflater.compress(body) + deflater.flush()
    assert len(compressed) >= len(body)

    # Call with always=True to force compression
    compress_request(prepped, always=True)

    # Body should now be compressed bytes
    assert isinstance(prepped.body, bytes)
    # Content-Encoding header should be set
    assert prepped.headers["Content-Encoding"] == "deflate"
    # Content-Length should match compressed size
    assert prepped.headers["Content-Length"] == str(len(prepped.body))
    # Decompress to verify integrity
    decompressed = zlib.decompress(prepped.body)
    assert decompressed == body
