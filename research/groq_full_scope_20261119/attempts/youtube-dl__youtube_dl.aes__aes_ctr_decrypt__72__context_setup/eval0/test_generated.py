import pytest
from youtube_dl.aes import aes_ctr_decrypt, aes_encrypt, BLOCK_SIZE_BYTES

class DummyCounter:
    """Counter that always returns the same 16‑byte block."""
    def __init__(self, block):
        self.block = block
    def next_value(self):
        return self.block

def test_aes_ctr_decrypt_roundtrip():
    # 16‑byte zero key and counter block
    key = [0] * 16
    counter_block = [0] * 16
    counter = DummyCounter(counter_block)

    # Plaintext: 32 bytes (two blocks)
    plaintext = list(range(32))
    # Encrypt each block with AES in ECB mode and XOR with counter block
    encrypted = []
    for i in range(0, len(plaintext), BLOCK_SIZE_BYTES):
        block = plaintext[i:i+BLOCK_SIZE_BYTES]
        block += [0] * (BLOCK_SIZE_BYTES - len(block))
        cipher_block = aes_encrypt(block, aes_ctr_decrypt.__globals__['key_expansion'](key))
        encrypted += xor(block, cipher_block)

    # Decrypt
    decrypted = aes_ctr_decrypt(encrypted, key, counter)
    assert decrypted == plaintext

def test_aes_ctr_decrypt_partial_block():
    key = [1] * 16
    counter_block = [2] * 16
    counter = DummyCounter(counter_block)

    # Plaintext of 20 bytes (one full block + 4 bytes)
    plaintext = list(range(20))
    # Encrypt
    encrypted = []
    for i in range(0, len(plaintext), BLOCK_SIZE_BYTES):
        block = plaintext[i:i+BLOCK_SIZE_BYTES]
        block += [0] * (BLOCK_SIZE_BYTES - len(block))
        cipher_block = aes_encrypt(block, aes_ctr_decrypt.__globals__['key_expansion'](key))
        encrypted += xor(block, cipher_block)

    # Decrypt
    decrypted = aes_ctr_decrypt(encrypted, key, counter)
    assert decrypted == plaintext

def test_aes_ctr_decrypt_empty_input():
    key = [0] * 16
    counter_block = [0] * 16
    counter = DummyCounter(counter_block)

    encrypted = []
    decrypted = aes_ctr_decrypt(encrypted, key, counter)
    assert decrypted == []
