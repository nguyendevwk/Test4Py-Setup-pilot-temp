import pytest
from youtube_dl.aes import key_expansion, BLOCK_SIZE_BYTES

def test_key_expansion_16byte_length_and_identity():
    # 16‑byte key (AES‑128)
    key = [0x2b, 0x7e, 0x15, 0x16,
           0x28, 0xae, 0xd2, 0xa6,
           0xab, 0xf7, 0x15, 0x88,
           0x09, 0xcf, 0x4f, 0x3c]
    expanded = key_expansion(key)
    # Expanded key for AES‑128 is 176 bytes
    assert len(expanded) == 176
    # The first 16 bytes of the expanded key are the original key
    assert expanded[:16] == key

def test_key_expansion_24byte_length_and_identity():
    # 24‑byte key (AES‑192)
    key = [0x8e, 0x73, 0xb0, 0xf7,
           0xda, 0x0e, 0x64, 0x52,
           0xc8, 0x10, 0xf3, 0x2b,
           0x80, 0x90, 0x79, 0xe5,
           0x62, 0xf8, 0xea, 0xd2,
           0x52, 0x2c, 0x6b, 0x7b]
    expanded = key_expansion(key)
    # Expanded key for AES‑192 is 208 bytes
    assert len(expanded) == 208
    # The first 24 bytes of the expanded key are the original key
    assert expanded[:24] == key

def test_key_expansion_input_immutability():
    key = [0x00] * 16
    key_copy = key[:]
    expanded = key_expansion(key)
    # Ensure the original key list was not modified
    assert key == key_copy
    # Ensure the expanded key is a new list
    assert expanded is not key
    # Changing the original key after expansion should not affect the result
    key[0] = 0xff
    assert expanded[0] == 0x00
