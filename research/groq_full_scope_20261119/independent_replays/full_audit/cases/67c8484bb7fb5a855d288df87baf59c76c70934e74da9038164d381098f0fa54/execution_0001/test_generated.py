import pytest
from youtube_dl.aes import inc

def test_increment_single_byte():
    # Increment a single byte that is not at maximum
    original = bytearray([0x01, 0x02, 0x03])
    result = inc(original)
    # The last byte should be incremented
    assert result == bytearray([0x01, 0x02, 0x04])
    # Original should remain unchanged
    assert original == bytearray([0x01, 0x02, 0x03])

def test_increment_with_carry():
    # Increment a byte that requires a carry to the previous byte
    original = bytearray([0x01, 0xFF, 0xFF])
    result = inc(original)
    # The last two bytes should wrap to 0, and the first byte incremented
    assert result == bytearray([0x02, 0x00, 0x00])
    # Original remains unchanged
    assert original == bytearray([0x01, 0xFF, 0xFF])

def test_increment_all_255():
    # Increment a bytearray where all bytes are 255
    original = bytearray([0xFF, 0xFF, 0xFF])
    result = inc(original)
    # All bytes should wrap to 0
    assert result == bytearray([0x00, 0x00, 0x00])
    # Original remains unchanged
    assert original == bytearray([0xFF, 0xFF, 0xFF])
