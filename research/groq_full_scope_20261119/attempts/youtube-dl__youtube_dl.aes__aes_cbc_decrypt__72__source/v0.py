import pytest
from youtube_dl.aes import aes_cbc_decrypt, BLOCK_SIZE_BYTES

# Helper to create a list of integers from bytes
def to_intlist(b: bytes):
    return list(b)

def test_decrypt_zero_plaintext():
    """Decrypting a ciphertext of all zeros with zero key and IV should yield zeros."""
    key = to_intlist(b'\x00' * 16)
    iv = to_intlist(b'\x00' * 16)
    # Ciphertext of 32 bytes (two blocks) all zeros
    ciphertext = to_intlist(b'\x00' * 32)
    plaintext = aes_cbc_decrypt(ciphertext, key, iv)
    assert plaintext == [0] * 32

def test_decrypt_partial_block():
    """Decrypting a ciphertext whose length is not a multiple of the block size should
    correctly truncate the output to the original length."""
    key = to_intlist(b'\x00' * 16)
    iv = to_intlist(b'\x00' * 16)
    # 20 bytes ciphertext (1 full block + 4 bytes)
    ciphertext = to_intlist(b'\x00' * 20)
    plaintext = aes_cbc_decrypt(ciphertext, key, iv)
    assert len(plaintext) == 20
    assert plaintext == [0] * 20

def test_invalid_key_length():
    """Providing a key of invalid length should raise a ValueError from key_expansion."""
    key = to_intlist(b'\x00' * 10)  # invalid length
    iv = to_intlist(b'\x00' * 16)
    ciphertext = to_intlist(b'\x00' * 16)
    with pytest.raises(ValueError):
        aes_cbc_decrypt(ciphertext, key, iv)
