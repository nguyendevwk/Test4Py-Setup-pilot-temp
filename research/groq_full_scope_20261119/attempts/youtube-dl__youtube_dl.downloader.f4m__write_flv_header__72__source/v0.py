import io
import pytest
from youtube_dl.downloader.f4m import write_flv_header

def test_write_flv_header_writes_correct_bytes_and_position(tmp_path):
    stream = io.BytesIO()
    write_flv_header(stream)
    # The header should be exactly 13 bytes long
    assert stream.getvalue() == b'FLV\x01\x05\x00\x00\x00\x09\x00\x00\x00\x00'
    # After writing, the stream position should be at the end of the header
    assert stream.tell() == 13

def test_write_flv_header_appends_to_existing_content(tmp_path):
    stream = io.BytesIO(b'PRE')
    write_flv_header(stream)
    # The header should be appended after the existing bytes
    assert stream.getvalue() == b'PREFLV\x01\x05\x00\x00\x00\x09\x00\x00\x00\x00'
    # Position should be at the end of the new content
    assert stream.tell() == 3 + 13

def test_write_flv_header_raises_on_closed_stream(tmp_path):
    stream = io.BytesIO()
    stream.close()
    with pytest.raises(ValueError):
        write_flv_header(stream)
