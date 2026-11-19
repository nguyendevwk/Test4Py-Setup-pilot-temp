import io
import struct
import pytest
from youtube_dl.downloader.f4m import write_metadata_tag

def test_write_metadata_tag_with_metadata(tmp_path):
    """When metadata is provided, the function writes the correct FLV script tag."""
    stream = io.BytesIO()
    metadata = b'{"title":"Test"}'
    write_metadata_tag(stream, metadata)
    data = stream.getvalue()

    # The first byte should be the SCRIPT_TAG marker (0x12)
    assert data[0] == 0x12

    # The next three bytes encode the length of the metadata
    length_bytes = data[1:4]
    expected_length = struct.pack('!I', len(metadata))[1:]
    assert length_bytes == expected_length

    # The following 7 bytes are the timestamp and stream ID (all zeros)
    assert data[4:11] == b'\x00\x00\x00\x00\x00\x00\x00'

    # The metadata itself should follow immediately
    assert data[11:11+len(metadata)] == metadata

    # The final 4 bytes encode the total tag size (header + metadata)
    total_size = 11 + len(metadata)
    total_size_bytes = data[-4:]
    assert total_size_bytes == struct.pack('!I', total_size)

def test_write_metadata_tag_without_metadata(tmp_path):
    """When metadata is empty or None, nothing should be written to the stream."""
    stream = io.BytesIO()
    write_metadata_tag(stream, None)
    assert stream.getvalue() == b''

    stream = io.BytesIO()
    write_metadata_tag(stream, b'')
    assert stream.getvalue() == b''

def test_write_metadata_tag_boundary_length(tmp_path):
    """Test that the length field correctly handles the maximum 24‑bit value."""
    # Create metadata of length 0xFFFFFF (the maximum value that fits in 24 bits)
    max_len = 0xFFFFFF
    metadata = b'a' * max_len
    stream = io.BytesIO()
    write_metadata_tag(stream, metadata)
    data = stream.getvalue()

    # Length field should be exactly 3 bytes representing 0xFFFFFF
    length_bytes = data[1:4]
    assert length_bytes == struct.pack('!I', max_len)[1:]

    # Total size should be header (11) + metadata length
    total_size = 11 + max_len
    total_size_bytes = data[-4:]
    assert total_size_bytes == struct.pack('!I', total_size)
