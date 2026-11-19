import io
import pytest
from youtube_dl.downloader.f4m import write_metadata_tag

def test_write_metadata_tag_empty():
    """When metadata is falsy, nothing is written to the stream."""
    stream = io.BytesIO()
    write_metadata_tag(stream, b"")
    assert stream.getvalue() == b""


def test_write_metadata_tag_small():
    """Small metadata writes correct FLV script tag header and data."""
    stream = io.BytesIO()
    metadata = b"test"
    write_metadata_tag(stream, metadata)
    data = stream.getvalue()

    # Expected structure:
    # 1 byte SCRIPT_TAG (0x12)
    # 3 bytes unsigned int 24 for metadata length
    # 7 bytes zero padding
    # metadata bytes
    # 4 bytes unsigned int for total tag size (header + metadata)
    assert data[0] == 0x12
    # metadata length encoded in 3 bytes
    assert data[1:4] == len(metadata).to_bytes(3, "big")
    assert data[4:11] == b"\x00\x00\x00\x00\x00\x00\x00"
    assert data[11:11 + len(metadata)] == metadata
    # total tag size: 11 (header) + len(metadata)
    total_size = int.from_bytes(data[11 + len(metadata):15], "big")
    assert total_size == 11 + len(metadata)


def test_write_metadata_tag_large():
    """Large metadata correctly encodes length and total size."""
    stream = io.BytesIO()
    metadata = b"a" * 1000  # 1000 bytes
    write_metadata_tag(stream, metadata)
    data = stream.getvalue()

    # Check header byte
    assert data[0] == 0x12
    # Metadata length in 3 bytes
    assert data[1:4] == len(metadata).to_bytes(3, "big")
    # Padding
    assert data[4:11] == b"\x00\x00\x00\x00\x00\x00\x00"
    # Metadata content
    assert data[11:11 + len(metadata)] == metadata
    # Total tag size
    total_size = int.from_bytes(data[11 + len(metadata):15], "big")
    assert total_size == 11 + len(metadata)
