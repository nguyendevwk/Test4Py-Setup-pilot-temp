import io
import struct
import pytest
from youtube_dl.downloader.f4m import write_metadata_tag

def _read_uint24(b: bytes) -> int:
    """Helper to decode a 3‑byte unsigned integer (big‑endian)."""
    return int.from_bytes(b, "big")

def _read_uint32(b: bytes) -> int:
    """Helper to decode a 4‑byte unsigned integer (big‑endian)."""
    return int.from_bytes(b, "big")

def test_write_metadata_tag_empty():
    """When metadata is falsy, nothing is written to the stream."""
    stream = io.BytesIO()
    write_metadata_tag(stream, b"")
    assert stream.getvalue() == b""


def test_write_metadata_tag_small():
    """Writes a small metadata payload correctly."""
    stream = io.BytesIO()
    metadata = b"abc"
    write_metadata_tag(stream, metadata)
    data = stream.getvalue()

    # Expected structure:
    # 1 byte: SCRIPT_TAG (0x12)
    # 3 bytes: length of metadata (0x00 0x00 0x03)
    # 7 bytes: zero padding
    # 3 bytes: metadata
    # 4 bytes: total tag size (FLV_TAG_HEADER_LEN + len(metadata) = 11 + 3 = 14)
    assert data[0:1] == b"\x12"
    assert _read_uint24(data[1:4]) == len(metadata)
    assert data[4:11] == b"\x00\x00\x00\x00\x00\x00\x00"
    assert data[11:14] == metadata
    assert _read_uint32(data[14:18]) == 11 + len(metadata)


def test_write_metadata_tag_large():
    """Writes a larger metadata payload and verifies length encoding."""
    stream = io.BytesIO()
    # 0x123456 = 1193046 bytes of metadata
    metadata = b"a" * 0x123456
    write_metadata_tag(stream, metadata)
    data = stream.getvalue()

    # Check the length field (3 bytes)
    length_bytes = data[1:4]
    assert _read_uint24(length_bytes) == len(metadata)

    # Check the zero padding
    assert data[4:11] == b"\x00\x00\x00\x00\x00\x00\x00"

    # Check the metadata content
    assert data[11:11 + len(metadata)] == metadata

    # Check the total tag size field (4 bytes)
    total_size = 11 + len(metadata)
    assert _read_uint32(data[11 + len(metadata):11 + len(metadata) + 4]) == total_size
