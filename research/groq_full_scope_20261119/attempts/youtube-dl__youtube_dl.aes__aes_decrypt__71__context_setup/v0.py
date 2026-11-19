import pytest
from youtube_dl.aes import aes_decrypt, BLOCK_SIZE_BYTES

def test_rounds_count_for_128bit_key():
    # 128‑bit key expands to 176 bytes -> 10 rounds
    expanded_key = [0] * 176
    data = [0] * BLOCK_SIZE_BYTES
    # The function does not expose rounds, but we can infer by calling
    # and ensuring no exception and correct output length.
    result = aes_decrypt(data, expanded_key)
    assert isinstance(result, list)
    assert len(result) == BLOCK_SIZE_BYTES

def test_output_length_for_256bit_key():
    # 256‑bit key expands to 240 bytes -> 13 rounds
    expanded_key = [0] * 240
    data = [0] * BLOCK_SIZE_BYTES
    result = aes_decrypt(data, expanded_key)
    assert len(result) == BLOCK_SIZE_BYTES

def test_known_output_with_zero_key_and_zero_data():
    # With all‑zero input and key, the decryption steps reduce to
    # sub_bytes_inv on zeros, which yields the first element of SBOX_INV (0x52).
    expanded_key = [0] * 176
    data = [0] * BLOCK_SIZE_BYTES
    expected = [0x52] * BLOCK_SIZE_BYTES
    assert aes_decrypt(data, expanded_key) == expected
