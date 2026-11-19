import pytest
from youtube_dl.aes import aes_encrypt, key_expansion
from youtube_dl.utils import bytes_to_intlist, intlist_to_bytes

# Test vector from NIST SP 800-38A
PLAINTEXT = bytes.fromhex("00112233445566778899aabbccddeeff")
KEY_128 = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
EXPECTED_CIPHERTEXT = bytes.fromhex("69c4e0d86a7b0430d8cdb78070b4c55a")

def test_aes_encrypt_known_vector():
    """Encrypt a single block with a known key and compare to the expected ciphertext."""
    expanded_key = key_expansion(KEY_128)
    data_ints = bytes_to_intlist(PLAINTEXT)
    cipher_ints = aes_encrypt(data_ints, expanded_key)
    cipher_bytes = intlist_to_bytes(cipher_ints)
    assert cipher_bytes == EXPECTED_CIPHERTEXT

def test_aes_encrypt_idempotent_with_same_input():
    """Encrypting the same block twice with the same key yields the same ciphertext."""
    expanded_key = key_expansion(KEY_128)
    data_ints = bytes_to_intlist(PLAINTEXT)
    first = aes_encrypt(data_ints, expanded_key)
    second = aes_encrypt(data_ints, expanded_key)
    assert first == second

def test_aes_encrypt_invalid_key_length_raises():
    """Providing an expanded key whose length is not a multiple of 16 should raise an error."""
    expanded_key = key_expansion(KEY_128)[:-1]  # truncate to invalid length
    data_ints = bytes_to_intlist(PLAINTEXT)
    with pytest.raises(ValueError):
        aes_encrypt(data_ints, expanded_key)
