import pytest
from youtube_dl.aes import aes_encrypt, key_expansion
from youtube_dl.utils import bytes_to_intlist, intlist_to_bytes

# Test vectors from NIST SP 800-38A
PLAINTEXT = bytes.fromhex("00112233445566778899aabbccddeeff")
KEY_128 = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
EXPECTED_CIPHERTEXT = bytes.fromhex("69c4e0d86a7b0430d8cdb78070b4c55a")

def test_aes_encrypt_128bit_vector():
    """Verify that aes_encrypt produces the expected ciphertext for a 128‑bit key."""
    expanded = key_expansion(KEY_128)
    data_ints = bytes_to_intlist(PLAINTEXT)
    cipher_ints = aes_encrypt(data_ints, expanded)
    cipher_bytes = intlist_to_bytes(cipher_ints)
    assert cipher_bytes == EXPECTED_CIPHERTEXT

def test_aes_encrypt_invalid_key_length():
    """aes_encrypt should raise a ValueError when the expanded key length is invalid."""
    # Create an expanded key with wrong length (e.g., 10 bytes)
    bad_expanded = [0] * 10
    data_ints = bytes_to_intlist(PLAINTEXT)
    with pytest.raises(ValueError):
        aes_encrypt(data_ints, bad_expanded)

def test_aes_encrypt_boundary_empty_input(tmp_path):
    """Encrypting an empty block should raise an error due to insufficient data length."""
    expanded = key_expansion(KEY_128)
    empty_data = []
    with pytest.raises(IndexError):
        aes_encrypt(empty_data, expanded)
