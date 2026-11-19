import pytest
from youtube_dl.aes import aes_encrypt, BLOCK_SIZE_BYTES

def test_aes_encrypt_zero_block_and_key():
    """Encrypt a block of all zeros with an all‑zero key."""
    data = [0x00] * BLOCK_SIZE_BYTES
    expanded_key = [0x00] * 176  # 10 rounds for 128‑bit key
    cipher = aes_encrypt(data, expanded_key)
    assert isinstance(cipher, list)
    assert len(cipher) == BLOCK_SIZE_BYTES
    # With all‑zero key the first round key addition leaves the state unchanged,
    # but subsequent rounds change it, so the result cannot be all zeros.
    assert cipher != [0x00] * BLOCK_SIZE_BYTES

def test_aes_encrypt_ff_block_and_zero_key():
    """Encrypt a block of all 0xFF with an all‑zero key."""
    data = [0xFF] * BLOCK_SIZE_BYTES
    expanded_key = [0x00] * 176
    cipher = aes_encrypt(data, expanded_key)
    assert isinstance(cipher, list)
    assert len(cipher) == BLOCK_SIZE_BYTES
    # The output should not be identical to the input.
    assert cipher != data

def test_aes_encrypt_invalid_data_type():
    """Passing a non‑iterable data type should raise a TypeError."""
    data = "not a list"
    expanded_key = [0x00] * 176
    with pytest.raises(TypeError):
        aes_encrypt(data, expanded_key)
