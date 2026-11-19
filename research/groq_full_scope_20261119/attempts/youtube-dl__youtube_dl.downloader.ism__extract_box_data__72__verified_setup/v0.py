import io
import struct
import pytest
from youtube_dl.downloader.ism import extract_box_data

def build_box(box_type: bytes, payload: bytes) -> bytes:
    """Helper to build a box with given type and payload."""
    size = 8 + len(payload)
    return struct.pack(">I", size) + box_type + payload

def test_extract_single_box():
    """Extract data from a single top‑level box."""
    payload = b"hello world"
    box = build_box(b"abcd", payload)
    result = extract_box_data(box, [b"abcd"])
    assert result == payload

def test_extract_nested_box():
    """Extract data from a nested box sequence."""
    inner_payload = b"inner data"
    inner_box = build_box(b"efgh", inner_payload)
    outer_box = build_box(b"abcd", inner_box)
    result = extract_box_data(outer_box, [b"abcd", b"efgh"])
    assert result == inner_payload

def test_missing_box_raises():
    """When the requested box sequence is not present, an EOFError is raised."""
    payload = b"data"
    box = build_box(b"abcd", payload)
    with pytest.raises(EOFError):
        # The sequence requests a box that does not exist
        extract_box_data(box, [b"abcd", b"zzzz"])
