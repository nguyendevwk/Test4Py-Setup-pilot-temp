import pytest
from youtube_dl.aes import aes_cbc_encrypt, BLOCK_SIZE_BYTES, key_expansion, aes_encrypt, xor

def test_padding_and_block_count(tmp_path):
    # 10 bytes of data, key and iv of 16 bytes
    data = list(range(10))
    key = [0x00] * 16
    iv = [0x00] * 16

    encrypted = aes_cbc_encrypt(data, key, iv)

    # The output length must be a multiple of BLOCK_SIZE_BYTES
    assert len(encrypted) % BLOCK_SIZE_BYTES == 0
    # For 10 bytes input, we expect 16 bytes output
    assert len(encrypted) == BLOCK_SIZE_BYTES

    # The padding byte should be 6 (16-10)
    padding_value = encrypted[-1]
    assert padding_value == 6
    # All padding bytes should be the same
    assert all(b == padding_value for b in encrypted[-padding_value:])

def test_deterministic_output_and_iv_effect(tmp_path):
    data = [1, 2, 3, 4]
    key = [0x01] * 16
    iv1 = [0x00] * 16
    iv2 = [0xFF] * 16

    enc1 = aes_cbc_encrypt(data, key, iv1)
    enc2 = aes_cbc_encrypt(data, key, iv1)
    enc3 = aes_cbc_encrypt(data, key, iv2)

    # Same inputs produce same output
    assert enc1 == enc2
    # Different IV produces different output
    assert enc1 != enc3

def test_invalid_key_length_raises():
    data = [0] * 16
    key_short = [0x00] * 15  # invalid length
    iv = [0x00] * 16
    with pytest.raises(ValueError):
        aes_cbc_encrypt(data, key_short, iv)
