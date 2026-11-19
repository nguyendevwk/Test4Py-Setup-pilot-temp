import io
import struct
import pytest
from youtube_dl.downloader.f4m import FlvReader


def test_read_unsigned_and_string():
    # Construct a byte stream: unsigned int 0x01020304, unsigned long long 0x0102030405060708,
    # unsigned char 0xFF, string "hello" + null terminator
    data = struct.pack('!I Q B', 0x01020304, 0x0102030405060708, 0xFF) + b'hello\x00'
    reader = FlvReader(data)

    assert reader.read_unsigned_int() == 0x01020304
    assert reader.read_unsigned_long_long() == 0x0102030405060708
    assert reader.read_unsigned_char() == 0xFF
    assert reader.read_string() == b'hello'


def test_read_asrt_parsing():
    # Build a minimal ASRT box:
    # version (1 byte), flags (3 bytes), quality_entry_count (1 byte)
    # one quality string "q" + null
    # segment_run_count (4 bytes), one segment: first_segment (4 bytes), fragments_per_segment (4 bytes)
    asrt_bytes = (
        b'\x01'                      # version
        + b'\x00\x00\x00'            # flags
        + b'\x01'                    # quality_entry_count
        + b'q\x00'                   # quality string
        + struct.pack('!I', 1)       # segment_run_count
        + struct.pack('!I I', 5, 2)  # first_segment, fragments_per_segment
    )
    # Wrap in a box: size = 8 + len(asrt_bytes), type 'asrt'
    box_size = 8 + len(asrt_bytes)
    box = struct.pack('!I', box_size) + b'asrt' + asrt_bytes

    reader = FlvReader(box)
    bootstrap = reader.read_bootstrap_info()
    # The bootstrap contains one segment with first_segment=5 and fragments_per_segment=2
    assert bootstrap['segments'][0]['segment_run'] == [(5, 2)]


def test_read_box_info_extended_size():
    # Create a box with extended size: size field = 1, then 8-byte extended size
    # type 'abcd', data 'xyz'
    data = b'\x00\x00\x00\x01'          # size = 1 (extended)
    data += struct.pack('!Q', 8 + 4 + 4)  # extended size = header(8) + type(4) + data(4)
    data += b'abcd'                      # type
    data += b'xyz'                       # data
    reader = FlvReader(data)
    size, box_type, box_data = reader.read_box_info()
    assert size == 8 + 4 + 4
    assert box_type == b'abcd'
    assert box_data == b'xyz'
