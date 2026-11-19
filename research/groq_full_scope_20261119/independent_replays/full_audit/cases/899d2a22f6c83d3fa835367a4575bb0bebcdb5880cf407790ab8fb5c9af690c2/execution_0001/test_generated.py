import io
import struct
import pytest
from youtube_dl.downloader.ism import extract_box_data, u32

def build_box(box_type: bytes, payload: bytes) -> bytes:
    """Helper to build a box with 4‑byte size header."""
    size = 8 + len(payload)
    return struct.pack(">I", size) + box_type + payload

def test_extract_simple_box():
    """Extract a single box that matches the requested sequence."""
    payload = b"hello world"
    box = build_box(b"abcd", payload)
    result = extract_box_data(box, [b"abcd"])
    assert result == payload

def test_extract_nested_box():
    """Extract a nested box by providing a sequence of box types."""
    inner_payload = b"inner data"
    inner_box = build_box(b"efgh", inner_payload)
    outer_box = build_box(b"abcd", inner_box)
    result = extract_box_data(outer_box, [b"abcd", b"efgh"])
    assert result == inner_payload

def test_extract_box_not_found_raises():
    """When the requested box sequence is not present, a struct error is raised."""
    payload = b"data"
    box = build_box(b"abcd", payload)
    with pytest.raises(struct.error):
        extract_box_data(box, [b"zzzz"])
