import io
import pytest
from youtube_dl.downloader.f4m import write_flv_header

def test_write_flv_header_basic():
    """The header should match the expected FLV header bytes."""
    stream = io.BytesIO()
    write_flv_header(stream)
    expected = b'FLV\x01\x05\x00\x00\x00\x09\x00\x00\x00\x00'
    assert stream.getvalue() == expected, "Header bytes do not match expected FLV header"

def test_write_flv_header_multiple_calls():
    """Calling the function multiple times should append headers sequentially."""
    stream = io.BytesIO()
    write_flv_header(stream)
    write_flv_header(stream)
    expected = b'FLV\x01\x05\x00\x00\x00\x09\x00\x00\x00\x00' * 2
    assert stream.getvalue() == expected, "Multiple headers not concatenated correctly"

def test_write_flv_header_stream_type(tmp_path):
    """The function should accept any writable binary stream; here we test with a file."""
    file_path = tmp_path / "header.flv"
    with open(file_path, "wb") as f:
        write_flv_header(f)
    with open(file_path, "rb") as f:
        data = f.read()
    expected = b'FLV\x01\x05\x00\x00\x00\x09\x00\x00\x00\x00'
    assert data == expected, "File stream did not receive the correct FLV header"
