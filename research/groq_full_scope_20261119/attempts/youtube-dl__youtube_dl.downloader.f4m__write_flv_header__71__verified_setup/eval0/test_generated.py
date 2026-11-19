import io
import pytest
from youtube_dl.downloader.f4m import write_flv_header

def test_write_flv_header_writes_expected_bytes():
    """The header should match the FLV specification bytes."""
    stream = io.BytesIO()
    write_flv_header(stream)
    expected = b'FLV\x01\x05\x00\x00\x00\x09\x00\x00\x00\x00'
    assert stream.getvalue() == expected, "Header bytes do not match expected FLV header"

def test_write_flv_header_updates_stream_position():
    """After writing, the stream position should be at the end of the header."""
    stream = io.BytesIO()
    write_flv_header(stream)
    # Header length is 12 bytes
    assert stream.tell() == 12, "Stream position should be at the end of the header"

def test_write_flv_header_is_idempotent_on_same_stream():
    """Writing the header twice should append a second header, not overwrite."""
    stream = io.BytesIO()
    write_flv_header(stream)
    write_flv_header(stream)
    expected = b'FLV\x01\x05\x00\x00\x00\x09\x00\x00\x00\x00' * 2
    assert stream.getvalue() == expected, "Header was not appended correctly on second write"
