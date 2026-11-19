import io
import struct
import pytest
from youtube_dl.downloader.f4m import FlvReader, DataTruncatedError

def test_read_bytes_truncation():
    # Create a reader with only 3 bytes
    r = FlvReader(b'\x01\x02\x03')
    # Reading 3 bytes succeeds
    assert r.read_bytes(3) == b'\x01\x02\x03'
    # Subsequent read of 1 byte should raise DataTruncatedError
    with pytest.raises(DataTruncatedError) as excinfo:
        r.read_bytes(1)
    assert 'need 1 bytes while only 0 bytes got' in str(excinfo.value)

def test_read_unsigned_int_and_long_long():
    # Construct bytes: 4-byte int 0x01020304 and 8-byte long long 0x05060708090A0B0C
    data = struct.pack('!I Q', 0x01020304, 0x05060708090A0B0C)
    r = FlvReader(data)
    assert r.read_unsigned_int() == 0x01020304
    assert r.read_unsigned_long_long() == 0x05060708090A0B0C

def test_read_box_info_with_extended_size():
    # Box header: size=1 (extended), type='abcd', extended size=20, data='12345678'
    header = struct.pack('!I 4s Q', 1, b'abcd', 20)
    data = header + b'12345678'
    r = FlvReader(data)
    size, box_type, box_data = r.read_box_info()
    # Extended size includes header; data length should be size - header_end (16)
    assert size == 20
    assert box_type == b'abcd'
    assert box_data == b'12345678'
