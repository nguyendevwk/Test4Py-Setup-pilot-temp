import pytest
from youtube_dl.aes import (
    aes_ctr_decrypt,
    aes_encrypt,
    key_expansion,
    xor,
    BLOCK_SIZE_BYTES,
)

class DummyCounter:
    """Counter that returns a 16‑byte block of the current counter value."""
    def __init__(self, start=0):
        self.value = start

    def next_value(self):
        block = [(self.value >> (8 * i)) & 0xFF for i in range(16)]
        self.value += 1
        return block

def test_aes_ctr_decrypt_normal():
    key = [i for i in range(16)]  # 16‑byte key
    data = [i % 256 for i in range(20)]  # 20 bytes of data
    counter = DummyCounter(0)

    # Compute expected result manually
    expanded_key = key_expansion(key)
    block_count = int((len(data) + BLOCK_SIZE_BYTES - 1) // BLOCK_SIZE_BYTES)
    expected = []
    for i in range(block_count):
        counter_block = counter.next_value()
        block = data[i * BLOCK_SIZE_BYTES : (i + 1) * BLOCK_SIZE_BYTES]
        block += [0] * (BLOCK_SIZE_BYTES - len(block))
        cipher_counter_block = aes_encrypt(counter_block, expanded_key)
        expected += xor(block, cipher_counter_block)
    expected = expected[:len(data)]

    # Reset counter for decryption
    counter = DummyCounter(0)
    result = aes_ctr_decrypt(data, key, counter)
    assert result == expected

def test_aes_ctr_decrypt_boundary():
    key = [i for i in range(16)]
    data = [i % 256 for i in range(BLOCK_SIZE_BYTES)]  # exactly one block
    counter = DummyCounter(42)

    expanded_key = key_expansion(key)
    counter_block = counter.next_value()
    cipher_counter_block = aes_encrypt(counter_block, expanded_key)
    expected = xor(data, cipher_counter_block)

    # Reset counter for decryption
    counter = DummyCounter(42)
    result = aes_ctr_decrypt(data, key, counter)
    assert result == expected

def test_aes_ctr_decrypt_invalid_key_length():
    key = [i for i in range(10)]  # invalid length
    data = [0] * 16
    counter = DummyCounter()
    with pytest.raises(ValueError):
        aes_ctr_decrypt(data, key, counter)
