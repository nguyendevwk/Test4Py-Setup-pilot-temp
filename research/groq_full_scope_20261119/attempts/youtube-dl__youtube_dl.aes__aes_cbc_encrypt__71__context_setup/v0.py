import pytest
from youtube_dl.aes import aes_cbc_encrypt, BLOCK_SIZE_BYTES

# Known test vector from NIST SP 800-38A
# Key: 2b7e151628aed2a6abf7158809cf4f3c
# IV:  000102030405060708090a0b0c0d0e0f
# Plaintext: 6bc1bee22e409f96e93d7e117393172a
# Ciphertext: 7649abac8119b246cee98e9b12e9197d
KEY = [0x2b, 0x7e, 0x15, 0x16,
       0x28, 0xae, 0xd2, 0xa6,
       0xab, 0xf7, 0x15, 0x88,
       0x09, 0xcf, 0x4f, 0x3c]
IV = [0x00, 0x01, 0x02, 0x03,
      0x04, 0x05, 0x06, 0x07,
      0x08, 0x09, 0x0a, 0x0b,
      0x0c, 0x0d, 0x0e, 0x0f]
PLAINTEXT = [0x6b, 0xc1, 0xbe, 0xe2,
             0x2e, 0x40, 0x9f, 0x96,
             0xe9, 0x3d, 0x7e, 0x11,
             0x73, 0x93, 0x17, 0x2a]
EXPECTED_CIPHERTEXT = [0x76, 0x49, 0xab, 0xac,
                       0x81, 0x19, 0xb2, 0x46,
                       0xce, 0xe9, 0x8e, 0x9b,
                       0x12, 0xe9, 0x19, 0x7d]

def test_aes_cbc_encrypt_known_vector():
    """Encrypt a single block with a known key and IV."""
    ciphertext = aes_cbc_encrypt(PLAINTEXT, KEY, IV)
    assert ciphertext == EXPECTED_CIPHERTEXT

def test_aes_cbc_encrypt_padding_length():
    """Ensure that data shorter than a block is padded to one block."""
    data = [0x01]  # single byte
    key = [0x00] * 16
    iv = [0x00] * 16
    ciphertext = aes_cbc_encrypt(data, key, iv)
    # The ciphertext must be exactly one block (16 bytes)
    assert len(ciphertext) == BLOCK_SIZE_BYTES
    # Padding byte value should be 16 (0x10)
    assert ciphertext[-1] == 16

def test_aes_cbc_encrypt_empty_input():
    """Encrypting an empty input should produce one block of padding."""
    data = []
    key = [0x00] * 16
    iv = [0x00] * 16
    ciphertext = aes_cbc_encrypt(data, key, iv)
    assert len(ciphertext) == BLOCK_SIZE_BYTES
    assert all(b == 16 for b in ciphertext)
