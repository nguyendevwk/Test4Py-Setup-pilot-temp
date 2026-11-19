import io
import pytest
from youtube_dl.downloader.f4m import write_flv_header

def test_write_flv_header_writes_correct_bytes():
    """The header should be written exactly as the FLV specification."""
    stream = io.BytesIO()
    write_flv_header(stream)
    expected = b'FLV\x01\x05\x00\x00\x00\x09\x00\x00\x00\x00'
    assert stream.getvalue() == expected
    # The stream position should be at the end of the header
    assert stream.tell() == len(expected)

def test_write_flv_header_appends_to_existing_stream():
    """Header should be appended to any existing data in the stream."""
    stream = io.BytesIO(b'EXISTING')
    write_flv_header(stream)
    expected = b'EXISTING' + b'FLV\x01\x05\x00\x00\x00\x09\x00\x00\x00\x00'
    assert stream.getvalue() == expected
    # Position should be after the appended header
    assert stream.tell() == len(expected)

def test_write_flv_header_returns_none_and_is_idempotent():
    """The function should return None and writing twice appends two headers."""
    stream = io.BytesIO()
    result = write_flv_header(stream)
    assert result is None
    write_flv_header(stream)
    expected = b'FLV\x01\x05\x00\x00\x00\x09\x00\x00\x00\x00' * 2
    assert stream.getvalue() == expected
    assert stream.tell() == len(expected)
