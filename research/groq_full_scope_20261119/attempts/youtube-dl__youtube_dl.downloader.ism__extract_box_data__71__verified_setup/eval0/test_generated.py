import io
import struct
import pytest
from youtube_dl.downloader.ism import extract_box_data

# Helper to build a box: size (4 bytes, big-endian), type (4 bytes), payload
def make_box(box_type: bytes, payload: bytes) -> bytes:
    size = 8 + len(payload)
    return struct.pack(">I", size) + box_type + payload

def test_extract_single_box():
    """Extract a single box from a simple stream."""
    payload = b"hello world"
    box = make_box(b"abcd", payload)
    result = extract_box_data(box, [b"abcd"])
    assert result == payload

def test_extract_nested_boxes():
    """Extract a nested box by specifying a sequence of types."""
    inner_payload = b"inner data"
    inner_box = make_box(b"inner", inner_payload)
    outer_payload = inner_box  # outer contains the inner box
    outer_box = make_box(b"outer", outer_payload)
    # Extract the inner payload by specifying the outer and inner types
    result = extract_box_data(outer_box, [b"outer", b"inner"])
    assert result == inner_payload

def test_missing_box_raises():
    """When the requested box type is not present, an exception is raised."""
    payload = b"some data"
    box = make_box(b"abcd", payload)
    with pytest.raises(struct.error):
        extract_box_data(box, [b"xxxx"])
