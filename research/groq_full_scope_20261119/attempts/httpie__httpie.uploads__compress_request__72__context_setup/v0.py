import io
import zlib
import requests
from httpie.uploads import compress_request

def test_compress_request_with_string_body(tmp_path):
    # Create a request with a small string body that will be compressed
    body = "Hello, world!"
    req = requests.Request("POST", "http://example.com", data=body)
    prepared = req.prepare()
    # Ensure body is a string before compression
    assert isinstance(prepared.body, str)
    compress_request(prepared, always=False)
    # Body should now be bytes and compressed
    assert isinstance(prepared.body, bytes)
    # Content-Encoding header should be set
    assert prepared.headers["Content-Encoding"] == "deflate"
    # Content-Length should match compressed size
    assert int(prepared.headers["Content-Length"]) == len(prepared.body)
    # Verify that decompression yields original body
    decompressed = zlib.decompress(prepared.body).decode()
    assert decompressed == body

def test_compress_request_with_file_like_body(tmp_path):
    # Create a temporary file with content larger than 1 byte
    file_path = tmp_path / "data.txt"
    file_path.write_text("A" * 100)
    with open(file_path, "rb") as f:
        req = requests.Request("POST", "http://example.com", data=f)
        prepared = req.prepare()
        # Body should be a file-like object before compression
        assert hasattr(prepared.body, "read")
        compress_request(prepared, always=False)
        # After compression, body should be bytes
        assert isinstance(prepared.body, bytes)
        # Content-Encoding header should be set
        assert prepared.headers["Content-Encoding"] == "deflate"
        # Content-Length should match compressed size
        assert int(prepared.headers["Content-Length"]) == len(prepared.body)
        # Decompress and compare
        decompressed = zlib.decompress(prepared.body).decode()
        assert decompressed == "A" * 100

def test_compress_request_always_compresses_even_if_not_economical(tmp_path):
    # Create a request with a body that is already small; compression will increase size
    body = b"\x00\x01\x02\x03\x04"
    req = requests.Request("POST", "http://example.com", data=body)
    prepared = req.prepare()
    # Ensure body is bytes before compression
    assert isinstance(prepared.body, bytes)
    compress_request(prepared, always=True)
    # Body should still be bytes and compressed
    assert isinstance(prepared.body, bytes)
    # Content-Encoding header should be set
    assert prepared.headers["Content-Encoding"] == "deflate"
    # Content-Length should match compressed size
    assert int(prepared.headers["Content-Length"]) == len(prepared.body)
    # Decompress and compare to original
    decompressed = zlib.decompress(prepared.body)
    assert decompressed == body
