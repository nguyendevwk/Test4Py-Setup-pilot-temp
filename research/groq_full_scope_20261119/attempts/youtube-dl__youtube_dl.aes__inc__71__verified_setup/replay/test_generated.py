import pytest
from youtube_dl.aes import inc

def test_increment_normal():
    original = [0, 1, 2]
    result = inc(original)
    # Increment last byte
    assert result == [0, 1, 3]
    # Original list should remain unchanged
    assert original == [0, 1, 2]

def test_increment_overflow_single_byte():
    original = [255]
    result = inc(original)
    # 255 rolls over to 0
    assert result == [0]
    # Original list remains unchanged
    assert original == [255]

def test_increment_overflow_multiple_bytes():
    original = [255, 255, 255]
    result = inc(original)
    # All bytes roll over to 0
    assert result == [0, 0, 0]
    # Original list remains unchanged
    assert original == [255, 255, 255]
