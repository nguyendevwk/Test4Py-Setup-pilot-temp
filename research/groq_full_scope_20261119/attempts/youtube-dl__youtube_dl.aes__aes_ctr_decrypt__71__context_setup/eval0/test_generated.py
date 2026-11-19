import pytest
from youtube_dl.aes import aes_ctr_decrypt, aes_encrypt, BLOCK_SIZE_BYTES

class SimpleCounter:
    """Counter that returns incremental 16‑byte blocks starting from 0."""
    def __init__(self):
        self.i = 0

    def next_value(self):
        block = [0] * BLOCK_SIZE_BYTES
        for j in range(BLOCK_SIZE_BYTES):
            block[j] = (self.i >> (8 * (BLOCK_SIZE_BYTES - 1 - j))) & 0xFF
        self.i += 1
        return block

def test_aes_ctr_decrypt_roundtrip():
    key = [i for i in range(16)]  # 16‑byte key
    plaintext = [i % 256 for i in range(30)]  # 30 bytes, not a multiple of block size
    counter = SimpleCounter()

    # Encrypt plaintext using the same counter
    expanded_key = key
    # We need to use the same counter state as decryption, so reset counter
    counter_enc = SimpleCounter()
    cipher = []
    block_count = (len(plaintext) + BLOCK_SIZE_BYTES - 1) // BLOCK_SIZE_BYTES
    for i in range(block_count):
        counter_block = counter_enc.next_value()
        block = plaintext[i * BLOCK_SIZE_BYTES:(i + 1) * BLOCK_SIZE_BYTES]
        block += [0] * (BLOCK_SIZE_BYTES - len(block))
        cipher_block = aes_encrypt(counter_block, key)
        cipher += [b ^ c for b, c in zip(block, cipher_block)]
    cipher = cipher[:len(plaintext)]

    # Decrypt
    counter_dec = SimpleCounter()
    decrypted = aes_ctr_decrypt(cipher, key, counter_dec)

    assert decrypted == plaintext, "Decrypted data should match original plaintext"

def test_aes_ctr_decrypt_empty_input():
    key = [0] * 16
    counter = SimpleCounter()
    result = aes_ctr_decrypt([], key, counter)
    assert result == [], "Decrypting empty data should return an empty list"

def test_aes_ctr_decrypt_invalid_counter():
    key = [0] * 16
    counter = object()  # does not have next_value
    with pytest.raises(AttributeError):
        aes_ctr_decrypt([0], key, counter)
