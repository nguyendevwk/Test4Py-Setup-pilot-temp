import io
import struct
import pytest
from youtube_dl.downloader.f4m import FlvReader

def build_box(box_type: bytes, payload: bytes) -> bytes:
    size = 8 + len(payload)
    return struct.pack('!I4s', size, box_type) + payload

def test_read_box_info_basic(tmp_path):
    payload = b'hello\x00world\x00'
    box = build_box(b'test', payload)
    reader = FlvReader(box)
    size, btype, data = reader.read_box_info()
    assert size == 8 + len(payload)
    assert btype == b'test'
    assert data == payload

def test_read_asrt_parsing(tmp_path):
    # Construct an asrt box with 1 quality entry and 1 segment
    quality = b'quality\x00'
    seg_payload = struct.pack('!I I', 5, 3)  # first_segment=5, fragments_per_segment=3
    payload = struct.pack('!B', 1) + quality + struct.pack('!I', 1) + seg_payload
    box = build_box(b'asrt', payload)
    reader = FlvReader(box)
    result = reader.read_asrt()
    assert result == {'segment_run': [(5, 3)]}

def test_read_afrt_and_abst(tmp_path):
    # Build afrt box: 1 fragment with duration 0 (discontinuity)
    frag_payload = (
        struct.pack('!I', 10) +                # first
        struct.pack('!Q', 123456789) +         # first_ts
        struct.pack('!I', 0) +                # duration
        struct.pack('!B', 2)                  # discontinuity_indicator
    )
    afrt_payload = struct.pack('!B', 1) + struct.pack('!I', 1) + frag_payload
    afrt_box = build_box(b'afrt', afrt_payload)

    # Build abst box containing the afrt box
    abst_payload = (
        struct.pack('!B', 1) +                # version
        b'\x00\x00\x00' +                    # flags
        struct.pack('!I', 1) +                # BootstrapinfoVersion
        struct.pack('!B', 0x20) +             # flags with live bit set
        struct.pack('!I', 1000) +             # time scale
        struct.pack('!Q', 0) +                # CurrentMediaTime
        struct.pack('!Q', 0) +                # SmpteTimeCodeOffset
        b'movie\x00' +                        # MovieIdentifier
        struct.pack('!B', 0) +                # server_count
        struct.pack('!B', 0) +                # quality_count
        b'' +                                 # DrmData
        b'' +                                 # MetaData
        struct.pack('!B', 0) +                # segments_count
        struct.pack('!B', 1) +                # fragments_run_count
        afrt_box
    )
    abst_box = build_box(b'abst', abst_payload)

    # Read bootstrap info
    reader = FlvReader(abst_box)
    result = reader.read_bootstrap_info()
    assert result['live'] is True
    assert len(result['fragments']) == 1
    frag = result['fragments'][0][0]
    assert frag['first'] == 10
    assert frag['ts'] == 123456789
    assert frag['duration'] == 0
    assert frag['discontinuity_indicator'] == 2
