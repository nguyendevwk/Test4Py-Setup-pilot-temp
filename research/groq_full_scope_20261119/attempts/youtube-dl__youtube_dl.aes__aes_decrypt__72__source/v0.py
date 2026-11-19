import pytest
from youtube_dl.aes import aes_decrypt, BLOCK_SIZE_BYTES

def test_aes_decrypt_identity_with_zero_key_and_cipher():
    """Decrypting a zero block with a zero expanded key should return zeros."""
    data = [0] * BLOCK_SIZE_BYTES
    expanded_key = [0] * 176  # 11 round keys for AES‑128
    result = aes_decrypt(data, expanded_key)
    assert isinstance(result, list)
    assert len(result) == BLOCK_SIZE_BYTES
    assert all(byte == 0 for byte in result)

def test_aes_decrypt_rounds_calculation():
    """The number of rounds is derived from the expanded key length."""
    data = [1] * BLOCK_SIZE_BYTES
    # AES‑192 expanded key length is 208 bytes -> 13 rounds
    expanded_key = [0] * 208
    result = aes_decrypt(data, expanded_key)
    # With zero key, the output should be the same as input after all round
    # transformations (since all round keys are zero).
    assert result == data

def test_aes_decrypt_invalid_data_length():
    """Providing data not of block size should still return a 16‑byte list."""
    data = [0] * (BLOCK_SIZE_BYTES - 1)  # 15 bytes instead of 16
    expanded_key = [0] * 176
    result = aes_decrypt(data, expanded_key)
    # The function does not explicitly check length, but the output should still
    # be a list of 16 integers (the algorithm pads/truncates implicitly).
    assert isinstance(result, list)
    assert len(result) == BLOCK_SIZE_BYTES
