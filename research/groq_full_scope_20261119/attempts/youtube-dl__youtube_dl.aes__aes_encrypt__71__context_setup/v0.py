import pytest
from youtube_dl.aes import aes_encrypt, BLOCK_SIZE_BYTES

def test_aes_encrypt_returns_list_of_ints():
    """Normal case: data and expanded_key are 16 and 176 bytes of zeros."""
    data = [0] * BLOCK_SIZE_BYTES
    expanded_key = [0] * (BLOCK_SIZE_BYTES * 11)  # 176 bytes for 128‑bit key
    cipher = aes_encrypt(data, expanded_key)
    assert isinstance(cipher, list)
    assert len(cipher) == BLOCK_SIZE_BYTES
    assert all(isinstance(x, int) for x in cipher)

def test_aes_encrypt_with_empty_input():
    """Boundary case: empty data list should return an empty list."""
    data = []
    expanded_key = [0] * (BLOCK_SIZE_BYTES * 11)
    cipher = aes_encrypt(data, expanded_key)
    assert cipher == []

def test_aes_encrypt_raises_on_invalid_key_type():
    """Error case: passing a non‑iterable expanded_key should raise TypeError."""
    data = [0] * BLOCK_SIZE_BYTES
    expanded_key = None  # not iterable
    with pytest.raises(TypeError):
        aes_encrypt(data, expanded_key)
