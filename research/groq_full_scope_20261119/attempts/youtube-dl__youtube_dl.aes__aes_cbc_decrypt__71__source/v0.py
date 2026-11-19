import pytest
from Crypto.Cipher import AES
from youtube_dl.aes import aes_cbc_decrypt, BLOCK_SIZE_BYTES

# Helper to convert bytes to int list
def bytes_to_intlist(b: bytes):
    return list(b)

# Helper to convert int list to bytes
def intlist_to_bytes(l):
    return bytes(l)

def test_aes_cbc_decrypt_normal():
    # 16‑byte plaintext, key and IV all zeros
    plaintext = b"1234567890abcdef"
    key = b"\x00" * 16
    iv = b"\x00" * 16

    # Encrypt with PyCryptodome to get expected ciphertext
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(plaintext)

    # Convert to int lists for the target function
    data_ints = bytes_to_intlist(ciphertext)
    key_ints = bytes_to_intlist(key)
    iv_ints = bytes_to_intlist(iv)

    # Decrypt using the target function
    decrypted_ints = aes_cbc_decrypt(data_ints, key_ints, iv_ints)
    decrypted = intlist_to_bytes(decrypted_ints)

    assert decrypted == plaintext, "Decrypted data does not match original plaintext"

def test_aes_cbc_decrypt_boundary():
    # 20‑byte plaintext (not a multiple of block size)
    plaintext = b"Hello, world! 1234"
    key = b"\x01" * 16
    iv = b"\x02" * 16

    # Encrypt with PyCryptodome
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(plaintext + b"\x00" * (BLOCK_SIZE_BYTES - len(plaintext) % BLOCK_SIZE_BYTES))

    # Truncate ciphertext to original length
    ciphertext = ciphertext[:len(plaintext)]

    data_ints = bytes_to_intlist(ciphertext)
    key_ints = bytes_to_intlist(key)
    iv_ints = bytes_to_intlist(iv)

    decrypted_ints = aes_cbc_decrypt(data_ints, key_ints, iv_ints)
    decrypted = intlist_to_bytes(decrypted_ints)

    assert decrypted == plaintext, "Boundary decryption failed: output mismatch"

def test_aes_cbc_decrypt_empty():
    # Empty data should return empty list
    key = b"\x00" * 16
    iv = b"\x00" * 16
    data_ints = []

    result = aes_cbc_decrypt(data_ints, bytes_to_intlist(key), bytes_to_intlist(iv))
    assert result == [], "Decryption of empty data should return an empty list"
