import pytest
from youtube_dl.aes import aes_ctr_decrypt, BLOCK_SIZE_BYTES, key_expansion, aes_encrypt, xor

class DummyCounter:
    """Counter that returns a fixed 16‑byte block."""
    def __init__(self, block):
        self.block = block
    def next_value(self):
        return self.block

def test_decrypt_identity_with_zero_key_and_counter():
    """When key and counter are zero, decryption should return the original data."""
    key = [0] * 16
    counter_block = [0] * 16
    counter = DummyCounter(counter_block)

    # Prepare data: 30 bytes (not a multiple of 16)
    data = list(range(30))
    # Encrypt: in CTR mode encryption is XOR with counter block
    # Since counter block is zeros, ciphertext equals plaintext
    ciphertext = data.copy()

    decrypted = aes_ctr_decrypt(ciphertext, key, counter)
    assert decrypted == data, "Decrypted data should match original when key and counter are zero"

def test_decrypt_with_non_multiple_block_and_incrementing_counter():
    """Decryption should correctly handle data whose length is not a multiple of the block size."""
    key = [i % 256 for i in range(16)]
    # Counter that increments by 1 each call
    class IncrementingCounter:
        def __init__(self):
            self.value = 0
        def next_value(self):
            block = [(self.value + i) % 256 for i in range(16)]
            self.value += 1
            return block
    counter = IncrementingCounter()

    # Prepare plaintext of 45 bytes
    plaintext = list(range(45))
    # Encrypt manually using CTR mode
    expanded_key = key_expansion(key)
    ciphertext = []
    block_count = (len(plaintext) + BLOCK_SIZE_BYTES - 1) // BLOCK_SIZE_BYTES
    for i in range(block_count):
        counter_block = counter.next_value()
        block = plaintext[i * BLOCK_SIZE_BYTES: (i + 1) * BLOCK_SIZE_BYTES]
        block += [0] * (BLOCK_SIZE_BYTES - len(block))
        cipher_counter_block = aes_encrypt(counter_block, expanded_key)
        ciphertext += xor(block, cipher_counter_block)
    ciphertext = ciphertext[:len(plaintext)]

    # Reset counter for decryption
    counter = IncrementingCounter()
    decrypted = aes_ctr_decrypt(ciphertext, key, counter)
    assert decrypted == plaintext, "Decrypted data should match original plaintext"

def test_decrypt_with_invalid_key_length_raises():
    """Providing a key of invalid length should raise a ValueError from key_expansion."""
    key = [0] * 10  # invalid length
    counter_block = [0] * 16
    counter = DummyCounter(counter_block)
    data = [1, 2, 3]
    with pytest.raises(ValueError):
        aes_ctr_decrypt(data, key, counter)
