import pytest
from youtube_dl.aes import aes_encrypt, key_expansion
from youtube_dl.utils import bytes_to_intlist, intlist_to_bytes

# Test vectors from NIST SP 800-38A
# 1. 128‑bit key, 128‑bit plaintext
PLAINTEXT1 = bytes.fromhex("00112233445566778899aabbccddeeff")
KEY1 = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
EXPECTED_CIPHERTEXT1 = bytes.fromhex("69c4e0d86a7b0430d8cdb78070b4c55a")

# 2. 128‑bit key, all‑zero plaintext
PLAINTEXT2 = bytes.fromhex("00000000000000000000000000000000")
KEY2 = bytes.fromhex("00000000000000000000000000000000")
EXPECTED_CIPHERTEXT2 = bytes.fromhex("66e94bd4ef8a2c3b884cfa59ca342b2e")

def test_aes_encrypt_known_vector_1():
    """Encrypt a known plaintext with a known key and compare to expected ciphertext."""
    expanded_key = key_expansion(KEY1)
    data_ints = bytes_to_intlist(PLAINTEXT1)
    cipher_ints = aes_encrypt(data_ints, expanded_key)
    cipher_bytes = intlist_to_bytes(cipher_ints)
    assert cipher_bytes == EXPECTED_CIPHERTEXT1

def test_aes_encrypt_known_vector_2():
    """Encrypt all‑zero plaintext with all‑zero key and verify the result."""
    expanded_key = key_expansion(KEY2)
    data_ints = bytes_to_intlist(PLAINTEXT2)
    cipher_ints = aes_encrypt(data_ints, expanded_key)
    cipher_bytes = intlist_to_bytes(cipher_ints)
    assert cipher_bytes == EXPECTED_CIPHERTEXT2

def test_aes_encrypt_invalid_input_type():
    """Passing a non‑list data argument should raise a TypeError."""
    expanded_key = key_expansion(KEY1)
    with pytest.raises(TypeError):
        aes_encrypt("not a list", expanded_key)
