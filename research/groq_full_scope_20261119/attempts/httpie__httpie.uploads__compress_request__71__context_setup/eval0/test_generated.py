import io
import zlib
import requests
import pytest

from httpie.uploads import compress_request


def test_compress_request_with_string_body(tmp_path):
    # Prepare a request with a string body that compresses well
    body = "a" * 1000  # highly compressible
    req = requests.Request("POST", "http://example.com", data=body)
    prepared = req.prepare()

    compress_request(prepared, always=False)

    # Body should be compressed
    assert prepared.body is not None
    assert isinstance(prepared.body, bytes)
    # Content-Encoding header should be set
    assert prepared.headers.get("Content-Encoding") == "deflate"
    # Content-Length should match compressed size
    assert int(prepared.headers["Content-Length"]) == len(prepared.body)
    # Verify that the compressed data decompresses to original
    decompressed = zlib.decompress(prepared.body)
    assert decompressed.decode() == body


def test_compress_request_with_file_like_body(tmp_path):
    # Create a temporary file with content that compresses poorly
    file_path = tmp_path / "data.bin"
    file_path.write_bytes(b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09")  # random bytes
    with open(file_path, "rb") as f:
        req = requests.Request("POST", "http://example.com", data=f)
        prepared = req.prepare()

    compress_request(prepared, always=False)

    # Since data is not compressible, body should remain unchanged
    assert prepared.body is not None
    assert isinstance(prepared.body, bytes)
    assert prepared.body == file_path.read_bytes()
    # No Content-Encoding header should be added
    assert "Content-Encoding" not in prepared.headers
    assert "Content-Length" not in prepared.headers


def test_compress_request_with_always_flag(tmp_path):
    # Prepare a request with a body that is not compressible
    body = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09"
    req = requests.Request("POST", "http://example.com", data=body)
    prepared = req.prepare()

    compress_request(prepared, always=True)

    # Body should be compressed even though not economical
    assert prepared.body is not None
    assert isinstance(prepared.body, bytes)
    assert prepared.headers.get("Content-Encoding") == "deflate"
    assert int(prepared.headers["Content-Length"]) == len(prepared.body)
    # Decompress to verify integrity
    decompressed = zlib.decompress(prepared.body)
    assert decompressed == body
