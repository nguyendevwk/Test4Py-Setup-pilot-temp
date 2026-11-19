import pytest
from youtube_dl.aes import inc

def test_increment_single_byte():
    original = bytearray([0x00, 0x01, 0x02])
    result = inc(original)
    # The last byte should be incremented
    assert result == bytearray([0x00, 0x01, 0x03])
    # Original should remain unchanged
    assert original == bytearray([0x00, 0x01, 0x02])

def test_increment_with_carry():
    original = bytearray([0x00, 0xFF, 0xFF])
    result = inc(original)
    # The last byte rolls over to 0, carry to previous byte
    assert result == bytearray([0x00, 0x00, 0x00])
    # The second byte should have been incremented from 0xFF to 0x00
    assert result[1] == 0x00
    # Original remains unchanged
    assert original == bytearray([0x00, 0xFF, 0xFF])

def test_increment_all_255():
    original = bytearray([0xFF, 0xFF, 0xFF])
    result = inc(original)
    # All bytes should roll over to 0
    assert result == bytearray([0x00, 0x00, 0x00])
    # Original remains unchanged
    assert original == bytearray([0xFF, 0xFF, 0xFF])
