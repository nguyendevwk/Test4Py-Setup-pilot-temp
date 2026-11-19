import pytest
from youtube_dl.aes import key_expansion

# Test vector from NIST SP 800-38A (AES-128 key expansion)
# 16‑byte key: 2b7e151628aed2a6abf7158809cf4f3c
# Expanded key first 8 words (32 bytes) should be:
# 2b7e1516 28aed2a6 abf71588 09cf4f3c a0fafe17 88542cb1 23a33939 2a6c7605
TEST_KEY = [
    0x2b, 0x7e, 0x15, 0x16,
    0x28, 0xae, 0xd2, 0xa6,
    0xab, 0xf7, 0x15, 0x88,
    0x09, 0xcf, 0x4f, 0x3c
]
EXPECTED_WORDS = [
    0x2b7e1516, 0x28aed2a6, 0xabf71588, 0x09cf4f3c,
    0xa0fafe17, 0x88542cb1, 0x23a33939, 0x2a6c7605
]

def test_key_expansion_128bit():
    expanded = key_expansion(TEST_KEY)
    # The expanded key should be 176 bytes (44 words)
    assert len(expanded) == 176
    # Convert every 4 bytes to a 32‑bit word
    words = [int.from_bytes(expanded[i:i+4], 'big') for i in range(0, 32, 4)]
    assert words == EXPECTED_WORDS

def test_key_expansion_length():
    # For a 24‑byte key the expanded key should be 240 bytes
    key_24 = [i for i in range(24)]
    expanded = key_expansion(key_24)
    assert len(expanded) == 240
    # The first 6 words should match the original key words
    words = [int.from_bytes(expanded[i:i+4], 'big') for i in range(0, 24, 4)]
    expected = [int.from_bytes(key_24[i:i+4], 'big') for i in range(0, 24, 4)]
    assert words == expected

def test_key_expansion_invalid_length():
    # AES key must be 16, 24, or 32 bytes; other lengths should raise ValueError
    with pytest.raises(ValueError):
        key_expansion([0] * 15)
