import pytest
from youtube_dl.aes import aes_cbc_decrypt
from Crypto.Cipher import AES  # pycryptodome is expected to be available in the test environment

# Helper to convert bytes to list of ints
def bytes_to_intlist(b: bytes):
    return list(b)

# Test 1: Decrypt a known AES‑CBC ciphertext (normal case)
def test_aes_cbc_decrypt_known_vector():
    key = bytes([0x00] * 16)
    iv = bytes([0x00] * 16)
    plaintext = b"abcdefghijklmnop"  # 16 bytes
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(plaintext)

    # Convert ciphertext to list of ints as expected by aes_cbc_decrypt
    data = bytes_to_intlist(ciphertext)

    decrypted = aes_cbc_decrypt(data, bytes_to_intlist(key), bytes_to_intlist(iv))
    assert bytes(decrypted) == plaintext

# Test 2: Decrypt data whose length is not a multiple of the block size (boundary case)
def test_aes_cbc_decrypt_partial_block():
    key = bytes([0x01] * 16)
    iv = bytes([0x02] * 16)
    # Create a 20‑byte plaintext and encrypt it
    plaintext = b"1234567890abcdefghij"  # 20 bytes
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(plaintext[:16]) + cipher.encrypt(plaintext[16:])[:4]  # 20 bytes

    data = bytes_to_intlist(ciphertext)
    decrypted = aes_cbc_decrypt(data, bytes_to_intlist(key), bytes_to_intlist(iv))
    assert bytes(decrypted) == plaintext

# Test 3: Decrypt with an empty data list (error/edge case)
def test_aes_cbc_decrypt_empty_data():
    key = bytes([0x0f] * 16)
    iv = bytes([0x0e] * 16)
    data = []
    decrypted = aes_cbc_decrypt(data, bytes_to_intlist(key), bytes_to_intlist(iv))
    assert decrypted == []
