import pytest
from youtube_dl.aes import (
    aes_ctr_decrypt,
    aes_encrypt,
    key_expansion,
    bytes_to_intlist,
    intlist_to_bytes,
    BLOCK_SIZE_BYTES,
)

class SimpleCounter:
    """Counter that returns sequential 16‑byte blocks starting from zero."""
    def __init__(self):
        self.value = 0

    def next_value(self):
        block = [(self.value >> (8 * i)) & 0xFF for i in range(16)]
        self.value += 1
        return block

def test_aes_ctr_decrypt_roundtrip():
    # 32‑byte plaintext (two blocks)
    plaintext = b"Hello, world! 1234567890"
    assert len(plaintext) == 32
    key = b"thisisasecretkey1234567890abcd"[:16]  # 16‑byte key
    counter = SimpleCounter()

    # Encrypt manually using AES‑CTR logic
    expanded_key = key_expansion(key)
    ciphertext = []
    for i in range(2):
        counter_block = counter.next_value()
        block = bytes_to_intlist(plaintext[i * BLOCK_SIZE_BYTES:(i + 1) * BLOCK_SIZE_BYTES])
        cipher_block = aes_encrypt(counter_block, expanded_key)
        ciphertext += [b ^ c for b, c in zip(block, cipher_block)]

    # Reset counter for decryption
    counter = SimpleCounter()
    decrypted = aes_ctr_decrypt(ciphertext, key, counter)
    assert intlist_to_bytes(decrypted) == plaintext

def test_aes_ctr_decrypt_partial_block():
    # 20‑byte plaintext (not a multiple of block size)
    plaintext = b"Partial block test!"
    key = b"anothersecretkey"[:16]
    counter = SimpleCounter()

    # Encrypt manually
    expanded_key = key_expansion(key)
    ciphertext = []
    block_count = (len(plaintext) + BLOCK_SIZE_BYTES - 1) // BLOCK_SIZE_BYTES
    for i in range(block_count):
        counter_block = counter.next_value()
        block = bytes_to_intlist(plaintext[i * BLOCK_SIZE_BYTES:(i + 1) * BLOCK_SIZE_BYTES])
        block += [0] * (BLOCK_SIZE_BYTES - len(block))
        cipher_block = aes_encrypt(counter_block, expanded_key)
        ciphertext += [b ^ c for b, c in zip(block, cipher_block)]
    ciphertext = ciphertext[:len(plaintext)]

    # Reset counter for decryption
    counter = SimpleCounter()
    decrypted = aes_ctr_decrypt(ciphertext, key, counter)
    assert intlist_to_bytes(decrypted) == plaintext

def test_aes_ctr_decrypt_invalid_key_length():
    plaintext = b"Test data"
    key = b"short"  # invalid length
    counter = SimpleCounter()
    ciphertext = [0] * len(plaintext)
    with pytest.raises(ValueError):
        aes_ctr_decrypt(ciphertext, key, counter)
