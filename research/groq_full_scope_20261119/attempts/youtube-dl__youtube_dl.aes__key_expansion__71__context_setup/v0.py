import pytest
from youtube_dl.aes import key_expansion

# 16‑byte key from the AES specification
AES_128_KEY = [
    0x2b, 0x7e, 0x15, 0x16,
    0x28, 0xae, 0xd2, 0xa6,
    0xab, 0xf7, 0x15, 0x88,
    0x09, 0xcf, 0x4f, 0x3c
]

# 24‑byte key consisting of 0x00…0x17
AES_192_KEY = list(range(24))

# 32‑byte key consisting of 0x00…0x1f
AES_256_KEY = list(range(32))

def test_key_expansion_128_first_word():
    expanded = key_expansion(AES_128_KEY)
    # The first word of the expanded key (after the original key) should be
    # 0x2b, 0x28, 0xab, 0xd6 according to the AES specification.
    assert expanded[16:20] == [0x2b, 0x28, 0xab, 0xd6]
    # The expanded key must contain 176 bytes for a 128‑bit key.
    assert len(expanded) == 176

def test_key_expansion_192_length():
    expanded = key_expansion(AES_192_KEY)
    # A 192‑bit key expands to 208 bytes.
    assert len(expanded) == 208
    # The first word of the expanded key (after the original key) should be
    # 0x00, 0x01, 0x02, 0x03 for this particular key.
    assert expanded[24:28] == [0x00, 0x01, 0x02, 0x03]

def test_key_expansion_256_length_and_content():
    expanded = key_expansion(AES_256_KEY)
    # A 256‑bit key expands to 240 bytes.
    assert len(expanded) == 240
    # The first word of the expanded key (after the original key) should be
    # 0x00, 0x01, 0x02, 0x03 for this particular key.
    assert expanded[32:36] == [0x00, 0x01, 0x02, 0x03]
