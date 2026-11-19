import io
import zlib
import requests
import pytest
from httpie.uploads import compress_request


def test_compress_request_with_string_body(tmp_path):
    # Prepare a request with a string body that will compress
    body = "a" * 1000  # highly compressible
    req = requests.Request("POST", "http://example.com")
    prepped = req.prepare()
    prepped.body = body
    prepped.headers = {}

    compress_request(prepped, always=False)

    # Body should now be compressed
    assert isinstance(prepped.body, bytes)
    # Content-Encoding header should be set
    assert prepped.headers.get("Content-Encoding") == "deflate"
    # Content-Length should match compressed size
    assert int(prepped.headers["Content-Length"]) == len(prepped.body)
    # Verify that the compressed data decompresses to original
    decompressed = zlib.decompress(prepped.body)
    assert decompressed.decode() == body


def test_compress_request_with_file_like_body(tmp_path):
    # Create a temporary file with non‑compressible data
    file_path = tmp_path / "data.bin"
    file_path.write_bytes(b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09")

    with open(file_path, "rb") as f:
        req = requests.Request("POST", "http://example.com")
        prepped = req.prepare()
        prepped.body = f
        prepped.headers = {}

        compress_request(prepped, always=False)

        # Since data is not compressible, body should remain unchanged
        assert prepped.body is f
        assert "Content-Encoding" not in prepped.headers
        assert "Content-Length" not in prepped.headers


def test_compress_request_with_uncompressible_body_and_always_flag(tmp_path):
    # Prepare a request with a body that is not compressible
    body = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09"
    req = requests.Request("POST", "http://example.com")
    prepped = req.prepare()
    prepped.body = body
    prepped.headers = {}

    compress_request(prepped, always=True)

    # Body should now be compressed even though not economical
    assert isinstance(prepped.body, bytes)
    assert prepped.headers.get("Content-Encoding") == "deflate"
    assert int(prepped.headers["Content-Length"]) == len(prepped.body)
    # Decompress to verify integrity
    decompressed = zlib.decompress(prepped.body)
    assert decompressed == body
