import io
import struct
import pytest
from youtube_dl.downloader.ism import extract_box_data

# Helper to build a box: size (4 bytes big-endian), type (4 bytes), payload
def make_box(box_type: bytes, payload: bytes) -> bytes:
    size = 8 + len(payload)
    return struct.pack(">I", size) + box_type + payload

def test_extract_single_box():
    # Create a single box 'abcd' containing payload b'hello'
    payload = b"hello"
    box = make_box(b"abcd", payload)
    result = extract_box_data(box, [b"abcd"])
    assert result == payload

def test_extract_nested_boxes():
    # Create nested boxes: outer 'root', inner 'mid', innermost 'innr'
    innermost = make_box(b"innr", b"data")
    mid = make_box(b"mid ", innermost)
    root = make_box(b"root", mid)
    # Extract innermost payload
    result = extract_box_data(root, [b"root", b"mid ", b"innr"])
    assert result == b"data"

def test_missing_box_raises():
    # Box 'abcd' missing; should raise struct.error when unpacking size at EOF
    payload = b"test"
    box = make_box(b"abcd", payload)
    with pytest.raises(struct.error):
        extract_box_data(box, [b"xxxx"])
