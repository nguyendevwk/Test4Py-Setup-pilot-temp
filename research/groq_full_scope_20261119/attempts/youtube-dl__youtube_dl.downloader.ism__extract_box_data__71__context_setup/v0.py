import io
import struct
import pytest
from youtube_dl.downloader.ism import extract_box_data, u32

def build_box(box_type: bytes, payload: bytes) -> bytes:
    """Helper to build a box with the given type and payload."""
    size = 8 + len(payload)
    return struct.pack(">I4s", size, box_type) + payload

def test_extract_single_box():
    """Extract a single box from a simple stream."""
    payload = b"hello world"
    box = build_box(b"abcd", payload)
    result = extract_box_data(box, [b"abcd"])
    assert result == payload

def test_extract_nested_boxes():
    """Extract a nested box sequence from a stream with multiple levels."""
    inner_payload = b"inner data"
    inner_box = build_box(b"efgh", inner_payload)
    outer_payload = inner_box + b"extra"
    outer_box = build_box(b"abcd", outer_payload)
    result = extract_box_data(outer_box, [b"abcd", b"efgh"])
    assert result == inner_payload

def test_missing_box_raises():
    """When the requested box sequence is not present, the function should raise an error."""
    payload = b"no match"
    box = build_box(b"abcd", payload)
    with pytest.raises(Exception):
        extract_box_data(box, [b"zzzz"])
