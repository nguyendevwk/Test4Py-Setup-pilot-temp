import io
import pytest
from youtube_dl.downloader.f4m import write_metadata_tag

def test_write_metadata_tag_empty():
    """When metadata is falsy, nothing is written to the stream."""
    stream = io.BytesIO()
    write_metadata_tag(stream, None)
    assert stream.getvalue() == b""

def test_write_metadata_tag_small():
    """Small metadata writes the correct FLV script tag header and payload."""
    stream = io.BytesIO()
    metadata = b"hello"
    write_metadata_tag(stream, metadata)
    data = stream.getvalue()
    # SCRIPT_TAG byte
    assert data[0:1] == b'\x12'
    # 3‑byte length of metadata
    length_bytes = data[1:4]
    assert int.from_bytes(length_bytes, "big") == len(metadata)
    # 7 zero bytes
    assert data[4:11] == b'\x00\x00\x00\x00\x00\x00\x00'
    # metadata payload
    assert data[11:11+len(metadata)] == metadata
    # final unsigned int: FLV_TAG_HEADER_LEN (11) + metadata length
    final_len = int.from_bytes(data[11+len(metadata):11+len(metadata)+4], "big")
    assert final_len == 11 + len(metadata)

def test_write_metadata_tag_large():
    """Large metadata correctly encodes a 24‑bit length and final unsigned int."""
    stream = io.BytesIO()
    # 300 bytes of metadata to exceed 255 (max 8‑bit)
    metadata = b'a' * 300
    write_metadata_tag(stream, metadata)
    data = stream.getvalue()
    # 3‑byte length should be 300
    length_bytes = data[1:4]
    assert int.from_bytes(length_bytes, "big") == 300
    # final unsigned int should be 11 + 300 = 311
    final_len = int.from_bytes(data[11+len(metadata):11+len(metadata)+4], "big")
    assert final_len == 311
