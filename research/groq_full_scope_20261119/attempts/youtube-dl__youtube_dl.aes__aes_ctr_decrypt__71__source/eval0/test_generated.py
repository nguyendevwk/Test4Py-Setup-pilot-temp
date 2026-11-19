import pytest
from youtube_dl.aes import aes_ctr_decrypt, BLOCK_SIZE_BYTES

class SimpleCounter:
    """Counter that returns a 16‑byte block of the same integer each call."""
    def __init__(self, start=0):
        self.value = start

    def next_value(self):
        block = [self.value] * BLOCK_SIZE_BYTES
        self.value += 1
        return block

def test_empty_data_returns_empty_list():
    """Decrypting an empty list should return an empty list."""
    data = []
    key = [0] * 16  # 16‑byte key
    counter = SimpleCounter()
    result = aes_ctr_decrypt(data, key, counter)
    assert isinstance(result, list)
    assert result == []

def test_partial_block_decryption():
    """Decrypting data shorter than one block should return a list of the same length."""
    data = [1, 2, 3, 4, 5]  # 5 bytes, less than BLOCK_SIZE_BYTES
    key = [0] * 16
    counter = SimpleCounter()
    result = aes_ctr_decrypt(data, key, counter)
    assert len(result) == len(data)
    # Since the counter block is all zeros, the keystream is aes_encrypt([0]*16)
    # The exact values depend on the AES implementation, but the operation
    # should be deterministic: result[i] == data[i] ^ keystream[i]
    keystream = aes_ctr_decrypt([0]*BLOCK_SIZE_BYTES, key, SimpleCounter())[0:BLOCK_SIZE_BYTES]
    for i, (d, r) in enumerate(zip(data, result)):
        assert r == d ^ keystream[i]

def test_encrypt_decrypt_roundtrip():
    """Encrypting and then decrypting with the same key and counter should yield the original data."""
    plaintext = [i % 256 for i in range(50)]  # 50 bytes, spans multiple blocks
    key = [i % 256 for i in range(16)]       # 16‑byte key
    # Encrypt
    encrypt_counter = SimpleCounter()
    ciphertext = aes_ctr_decrypt(plaintext, key, encrypt_counter)
    # Decrypt
    decrypt_counter = SimpleCounter()
    recovered = aes_ctr_decrypt(ciphertext, key, decrypt_counter)
    assert recovered == plaintext
