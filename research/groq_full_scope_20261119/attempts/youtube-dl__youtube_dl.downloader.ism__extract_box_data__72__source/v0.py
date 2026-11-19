import io
import struct
import pytest
from youtube_dl.downloader.ism import extract_box_data

# Helper to build a box: size (4 bytes) + type (4 bytes) + payload
def make_box(box_type: bytes, payload: bytes) -> bytes:
    size = 8 + len(payload)
    return struct.pack(">I", size) + box_type + payload

def test_extract_simple_box():
    """Extract a single top‑level box."""
    payload = b"hello world"
    box = make_box(b"abcd", payload)
    result = extract_box_data(box, [b"abcd"])
    assert result == payload

def test_extract_nested_box():
    """Extract a box nested inside another box."""
    inner_payload = b"inner data"
    inner_box = make_box(b"efgh", inner_payload)
    outer_box = make_box(b"abcd", inner_box)
    result = extract_box_data(outer_box, [b"abcd", b"efgh"])
    assert result == inner_payload

def test_extract_missing_box_raises():
    """When the requested box sequence is not present, an EOFError is raised."""
    payload = b"data"
    box = make_box(b"abcd", payload)
    with pytest.raises(EOFError):
        extract_box_data(box, [b"abcd", b"zzzz"])
