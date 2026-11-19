import io
import struct
import pytest
from youtube_dl.downloader.f4m import write_metadata_tag, write_unsigned_int, write_unsigned_int_24

def test_write_metadata_tag_with_metadata(tmp_path):
    # Prepare a stream and metadata
    stream = io.BytesIO()
    metadata = b'hello'
    write_metadata_tag(stream, metadata)

    # Expected bytes:
    # SCRIPT_TAG
    # 24-bit length of metadata
    # 7 zero bytes
    # metadata
    # 32-bit FLV tag length (header + metadata)
    expected = bytearray()
    expected.append(0x12)  # SCRIPT_TAG
    expected.extend(struct.pack('!I', len(metadata))[1:])  # 24-bit length
    expected.extend(b'\x00\x00\x00\x00\x00\x00\x00')
    expected.extend(metadata)
    flv_tag_len = 11 + len(metadata)
    expected.extend(struct.pack('!I', flv_tag_len))

    assert stream.getvalue() == bytes(expected)

def test_write_metadata_tag_without_metadata(tmp_path):
    # When metadata is falsy, nothing should be written
    stream = io.BytesIO()
    write_metadata_tag(stream, None)
    write_metadata_tag(stream, b'')
    assert stream.getvalue() == b''

def test_write_metadata_tag_boundary_length(tmp_path):
    # Test with a metadata length that fits in 24 bits (max 0xFFFFFF)
    stream = io.BytesIO()
    metadata = b'a' * 0xFFFFFF  # 16,777,215 bytes
    write_metadata_tag(stream, metadata)

    # Verify header bytes
    data = stream.getvalue()
    assert data[0] == 0x12  # SCRIPT_TAG
    # 24-bit length should match metadata length
    length_bytes = data[1:4]
    assert struct.unpack('!I', b'\x00' + length_bytes)[0] == len(metadata)
    # The 7 zero bytes should follow
    assert data[4:11] == b'\x00\x00\x00\x00\x00\x00\x00'
    # Metadata should be present
    assert data[11:11+len(metadata)] == metadata
    # FLV tag length should be header + metadata
    flv_len = struct.unpack('!I', data[-4:])[0]
    assert flv_len == 11 + len(metadata)
