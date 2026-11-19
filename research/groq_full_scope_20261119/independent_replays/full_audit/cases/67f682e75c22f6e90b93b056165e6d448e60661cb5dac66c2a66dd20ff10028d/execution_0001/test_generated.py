import struct
import pytest
from youtube_dl.downloader.f4m import FlvReader, DataTruncatedError


def test_read_unsigned_int_and_string():
    # Construct a byte stream: unsigned int 0x01020304 followed by a string "test" and null terminator
    data = struct.pack('!I', 0x01020304) + b'test\x00'
    reader = FlvReader(data)

    # Verify unsigned int reading
    value = reader.read_unsigned_int()
    assert value == 0x01020304, f"Expected 0x01020304, got {value:#x}"

    # Verify string reading
    string = reader.read_string()
    assert string == b'test', f"Expected b'test', got {string}"


def test_read_bytes_truncation_raises():
    # Provide fewer bytes than requested
    data = b'\x01\x02'
    reader = FlvReader(data)

    # read_bytes should raise DataTruncatedError when insufficient data
    with pytest.raises(DataTruncatedError) as excinfo:
        reader.read_bytes(4)
    assert "need 4 bytes while only 2 bytes got" in str(excinfo.value)


def test_read_unsigned_long_long_and_unsigned_char():
    # Construct a byte stream: unsigned long long 0x0102030405060708 and unsigned char 0xFF
    data = struct.pack('!Q', 0x0102030405060708) + b'\xFF'
    reader = FlvReader(data)

    # Verify unsigned long long reading
    ull_value = reader.read_unsigned_long_long()
    assert ull_value == 0x0102030405060708, f"Expected 0x0102030405060708, got {ull_value:#x}"

    # Verify unsigned char reading
    uchar_value = reader.read_unsigned_char()
    assert uchar_value == 0xFF, f"Expected 0xFF, got {uchar_value:#x}"
