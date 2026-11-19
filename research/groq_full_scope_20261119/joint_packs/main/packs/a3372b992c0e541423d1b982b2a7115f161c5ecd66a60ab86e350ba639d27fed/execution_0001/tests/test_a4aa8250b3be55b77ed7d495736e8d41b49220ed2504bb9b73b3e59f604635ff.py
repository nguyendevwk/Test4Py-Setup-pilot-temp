import io
import pytest
from youtube_dl.downloader.f4m import write_flv_header

def test_write_flv_header_writes_correct_bytes(tmp_path):
    """The header should be written exactly as defined."""
    stream = io.BytesIO()
    write_flv_header(stream)
    expected = b'FLV\x01\x05\x00\x00\x00\x09\x00\x00\x00\x00'
    assert stream.getvalue() == expected

def test_write_flv_header_on_empty_stream(tmp_path):
    """Calling the function on an empty BytesIO should produce the header."""
    stream = io.BytesIO()
    write_flv_header(stream)
    assert stream.getvalue() == b'FLV\x01\x05\x00\x00\x00\x09\x00\x00\x00\x00'

def test_write_flv_header_raises_on_non_writable_stream():
    """If the stream does not provide a write method, an AttributeError should be raised."""
    class DummyStream:
        pass
    stream = DummyStream()
    with pytest.raises(AttributeError):
        write_flv_header(stream)
