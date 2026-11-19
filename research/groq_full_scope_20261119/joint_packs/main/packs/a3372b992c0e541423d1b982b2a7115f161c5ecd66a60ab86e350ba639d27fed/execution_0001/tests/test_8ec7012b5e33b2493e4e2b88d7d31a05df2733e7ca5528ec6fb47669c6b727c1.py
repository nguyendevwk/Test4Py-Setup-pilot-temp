import struct
import pytest
from youtube_dl.downloader.f4m import FlvReader, DataTruncatedError


def build_bootstrap(live_flag: bool) -> bytes:
    """
    Build a minimal bootstrap box containing one asrt and one afrt segment.
    """
    # Helper to build a box
    def box(box_type: bytes, payload: bytes) -> bytes:
        size = 8 + len(payload)
        return struct.pack("!I4s", size, box_type) + payload

    # Build asrt payload (empty segment list)
    asrt_payload = struct.pack("!B3sB", 0, b"\x00\x00\x00", 0)  # version, flags, quality_entry_count
    asrt_payload += struct.pack("!I", 0)  # segment_run_count
    asrt_box = box(b"asrt", asrt_payload)

    # Build afrt payload (empty fragment list)
    afrt_payload = struct.pack("!B3sI", 0, b"\x00\x00\x00", 0)  # version, flags, time_scale
    afrt_payload += struct.pack("!B", 0)  # quality_entry_count
    afrt_payload += struct.pack("!I", 0)  # fragments_count
    afrt_box = box(b"afrt", afrt_payload)

    # Build abst payload
    abst_payload = struct.pack("!B3sI", 0, b"\x00\x00\x00", 0)  # version, flags, bootstrapinfoVersion
    flags = 0x20 if live_flag else 0x00
    abst_payload += struct.pack("!B", flags)  # flags
    abst_payload += struct.pack("!I", 0)  # time_scale
    abst_payload += struct.pack("!Q", 0)  # CurrentMediaTime
    abst_payload += struct.pack("!Q", 0)  # SmpteTimeCodeOffset
    abst_payload += b"\x00"  # MovieIdentifier
    abst_payload += struct.pack("!B", 0)  # server_count
    abst_payload += struct.pack("!B", 0)  # quality_count
    abst_payload += b"\x00"  # DrmData
    abst_payload += b"\x00"  # MetaData
    abst_payload += struct.pack("!B", 1)  # segments_count
    abst_payload += asrt_box
    abst_payload += struct.pack("!B", 1)  # fragments_run_count
    abst_payload += afrt_box

    abst_box = box(b"abst", abst_payload)
    return abst_box


def test_read_bootstrap_info_parses_live_flag_and_segments():
    data = build_bootstrap(live_flag=True)
    reader = FlvReader(data)
    bootstrap = reader.read_bootstrap_info()
    assert bootstrap["live"] is True
    assert len(bootstrap["segments"]) == 1
    assert len(bootstrap["fragments"]) == 1
    # The asrt and afrt payloads are empty, so their internal lists should be empty
    assert bootstrap["segments"][0]["segment_run"] == []
    assert bootstrap["fragments"][0]["fragments"] == []


def test_read_bootstrap_info_parses_non_live_flag():
    data = build_bootstrap(live_flag=False)
    reader = FlvReader(data)
    bootstrap = reader.read_bootstrap_info()
    assert bootstrap["live"] is False
    assert len(bootstrap["segments"]) == 1
    assert len(bootstrap["fragments"]) == 1


def test_read_bytes_raises_on_truncated_data():
    # Create a box with declared size larger than actual payload
    payload = struct.pack("!I4s", 20, b"abst") + b"\x00" * 5  # size 20, but only 5 bytes payload
    reader = FlvReader(payload)
    with pytest.raises(DataTruncatedError):
        reader.read_bootstrap_info()
