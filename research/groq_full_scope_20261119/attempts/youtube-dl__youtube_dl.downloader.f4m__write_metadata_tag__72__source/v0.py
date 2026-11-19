import io
import pytest
from youtube_dl.downloader.f4m import write_metadata_tag

# Helper to read all bytes from a BytesIO stream
def read_stream(stream):
    stream.seek(0)
    return stream.read()

def test_write_metadata_tag_no_metadata():
    """When metadata is falsy, nothing should be written to the stream."""
    stream = io.BytesIO()
    write_metadata_tag(stream, None)
    assert read_stream(stream) == b"", "Stream should remain empty when metadata is None"

def test_write_metadata_tag_with_metadata():
    """Metadata should be written with correct header and length encoding."""
    stream = io.BytesIO()
    metadata = b"testdata"
    write_metadata_tag(stream, metadata)
    result = read_stream(stream)

    # Expected structure:
    # 1 byte SCRIPT_TAG (0x12)
    # 3 bytes unsigned int (length of metadata)
    # 7 bytes zero padding
    # metadata bytes
    # 4 bytes unsigned int (FLV_TAG_HEADER_LEN + len(metadata))
    assert result[0:1] == b'\x12', "SCRIPT_TAG byte missing"
    assert result[1:4] == b'\x00\x00\x08', "Incorrect metadata length encoding"
    assert result[4:11] == b'\x00\x00\x00\x00\x00\x00\x00', "Zero padding incorrect"
    assert result[11:19] == metadata, "Metadata bytes not written correctly"
    expected_tag_size = 11 + len(metadata)
    assert result[19:23] == expected_tag_size.to_bytes(4, 'big'), "Tag size incorrect"

def test_write_metadata_tag_boundary_length():
    """Test boundary condition with maximum 3-byte length (0xFFFFFF)."""
    stream = io.BytesIO()
    # Create metadata of length 0xFFFFFF (16777215 bytes)
    metadata = b'a' * 0xFFFFFF
    write_metadata_tag(stream, metadata)
    result = read_stream(stream)

    # Verify length bytes
    assert result[1:4] == b'\xFF\xFF\xFF', "Length bytes should be 0xFFFFFF"
    # Verify tag size (FLV_TAG_HEADER_LEN + metadata length)
    expected_tag_size = 11 + 0xFFFFFF
    assert result[19:23] == expected_tag_size.to_bytes(4, 'big'), "Tag size incorrect for max length"
