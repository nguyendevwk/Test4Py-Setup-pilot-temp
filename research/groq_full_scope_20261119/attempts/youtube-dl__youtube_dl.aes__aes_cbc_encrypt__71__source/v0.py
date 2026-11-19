import pytest
from youtube_dl.aes import aes_cbc_encrypt, BLOCK_SIZE_BYTES, key_expansion, aes_encrypt, xor

def test_padding_and_block_count(tmp_path):
    # 10 bytes of data, 16-byte block size -> padded to 16 bytes
    data = list(range(10))
    key = [0x00] * 16
    iv = [0x00] * 16
    encrypted = aes_cbc_encrypt(data, key, iv)
    # Output length must be a multiple of block size
    assert len(encrypted) % BLOCK_SIZE_BYTES == 0
    # For 10 bytes input, we expect exactly one block (16 bytes)
    assert len(encrypted) == BLOCK_SIZE_BYTES
    # The padding byte should be 6 (16-10)
    assert encrypted[-6:] == [6] * 6

def test_deterministic_output_with_fixed_inputs():
    data = [1, 2, 3, 4]
    key = [0x01] * 16
    iv = [0x02] * 16
    # Encrypt twice with same inputs
    out1 = aes_cbc_encrypt(data, key, iv)
    out2 = aes_cbc_encrypt(data, key, iv)
    assert out1 == out2
    # Changing IV changes output
    iv2 = [0x03] * 16
    out3 = aes_cbc_encrypt(data, key, iv2)
    assert out3 != out1

def test_invalid_key_length_raises():
    data = [0] * 16
    iv = [0] * 16
    # key must be 16, 24, or 32 bytes
    with pytest.raises(ValueError):
        aes_cbc_encrypt(data, [0x00] * 15, iv)
    with pytest.raises(ValueError):
        aes_cbc_encrypt(data, [0x00] * 17, iv)
