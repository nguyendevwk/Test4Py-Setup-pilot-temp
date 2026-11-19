import io
import struct
import pytest
from youtube_dl.downloader.f4m import FlvReader
from youtube_dl.compat import compat_struct_pack

def build_box(box_type: bytes, payload: bytes) -> bytes:
    """Construct a box with 32‑bit size header."""
    size = 8 + len(payload)
    return compat_struct_pack('!I4s', size, box_type) + payload

def test_read_box_info_basic():
    """Verify that read_box_info correctly parses a simple box."""
    payload = b'hello'
    box = build_box(b'abst', payload)
    reader = FlvReader(box)
    size, box_type, data = reader.read_box_info()
    assert size == 8 + len(payload)
    assert box_type == b'abst'
    assert data == payload

def test_read_asrt_minimal():
    """Test parsing of an ASRT box with no quality entries or segments."""
    # ASRT box payload: version(1) + flags(3) + quality_entry_count(1) + segment_run_count(4)
    payload = struct.pack('!B3sB', 0, b'\x00\x00\x00', 0) + struct.pack('!I', 0)
    box = build_box(b'asrt', payload)
    reader = FlvReader(box)
    result = reader.read_asrt()
    assert result == {'segment_run': []}

def test_read_afrt_minimal():
    """Test parsing of an AFRT box with no fragments."""
    # AFRT box payload: version(1) + flags(3) + time_scale(4) + quality_entry_count(1)
    # + fragments_count(4)
    payload = struct.pack('!B3sI', 0, b'\x00\x00\x00', 1000) + struct.pack('!B', 0)
    payload += struct.pack('!I', 0)  # fragments_count
    box = build_box(b'afrt', payload)
    reader = FlvReader(box)
    result = reader.read_afrt()
    assert result == {'fragments': []}
