import pytest
from youtube_dl.aes import inc

def test_increment_middle_byte():
    # Increment a byte that is not 255; only that byte should change
    original = bytearray([0x01, 0x02, 0x03])
    result = inc(original)
    assert result == bytearray([0x01, 0x02, 0x04]), "Only the last byte should be incremented"
    # Ensure original is unchanged (copy semantics)
    assert original == bytearray([0x01, 0x02, 0x03]), "Original data must remain unchanged"

def test_increment_with_carry():
    # Increment a byte that is 255, causing a carry to the previous byte
    original = bytearray([0x01, 0xFF, 0xFF])
    result = inc(original)
    assert result == bytearray([0x02, 0x00, 0x00]), "Carry should propagate to the most significant byte"
    # Ensure original is unchanged
    assert original == bytearray([0x01, 0xFF, 0xFF]), "Original data must remain unchanged"

def test_increment_all_255():
    # Increment when all bytes are 255; result should wrap to all zeros
    original = bytearray([0xFF, 0xFF, 0xFF])
    result = inc(original)
    assert result == bytearray([0x00, 0x00, 0x00]), "All 255 bytes should wrap to zeros"
    # Ensure original is unchanged
    assert original == bytearray([0xFF, 0xFF, 0xFF]), "Original data must remain unchanged"
