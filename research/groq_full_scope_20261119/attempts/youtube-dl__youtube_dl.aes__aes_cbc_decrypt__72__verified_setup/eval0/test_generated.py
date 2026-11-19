import pytest
from youtube_dl.aes import aes_cbc_decrypt

# Test vectors from NIST SP 800-38A
# Key: 2b7e151628aed2a6abf7158809cf4f3c
# IV:  000102030405060708090a0b0c0d0e0f
# Plaintext block 1: 6bc1bee22e409f96e93d7e117393172a
# Ciphertext block 1: 7649abac8119b246cee98e9b12e9197d
# Plaintext block 2: ae2d8a571e03ac9c9eb76fac45af8e51
# Ciphertext block 2: 5086cb9b507219ee95db113a917678b2

KEY = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6,
       0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]
IV = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
      0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f]
CIPHERTEXT_BLOCK1 = [0x76, 0x49, 0xab, 0xac, 0x81, 0x19, 0xb2, 0x46,
                     0xce, 0xe9, 0x8e, 0x9b, 0x12, 0xe9, 0x19, 0x7d]
CIPHERTEXT_BLOCK2 = [0x50, 0x86, 0xcb, 0x9b, 0x50, 0x72, 0x19, 0xee,
                     0x95, 0xdb, 0x11, 0x3a, 0x91, 0x76, 0x78, 0xb2]
PLAINTEXT_BLOCK1 = [0x6b, 0xc1, 0xbe, 0xe2, 0x2e, 0x40, 0x9f, 0x96,
                    0xe9, 0x3d, 0x7e, 0x11, 0x73, 0x93, 0x17, 0x2a]
PLAINTEXT_BLOCK2 = [0xae, 0x2d, 0x8a, 0x57, 0x1e, 0x03, 0xac, 0x9c,
                    0x9e, 0xb7, 0x6f, 0xac, 0x45, 0xaf, 0x8e, 0x51]

def test_full_block_decryption():
    """Decrypt a single 16‑byte block and verify the plaintext."""
    ciphertext = CIPHERTEXT_BLOCK1
    plaintext = aes_cbc_decrypt(ciphertext, KEY, IV)
    assert plaintext == PLAINTEXT_BLOCK1

def test_multiple_blocks_and_truncation():
    """Decrypt two blocks and verify that the function truncates to the
    original ciphertext length when the data is not a multiple of the
    block size."""
    ciphertext = CIPHERTEXT_BLOCK1 + CIPHERTEXT_BLOCK2
    # Append 4 extra bytes to make length 36 (not a multiple of 16)
    ciphertext += [0x00, 0x01, 0x02, 0x03]
    plaintext = aes_cbc_decrypt(ciphertext, KEY, IV)
    expected = PLAINTEXT_BLOCK1 + PLAINTEXT_BLOCK2 + [0x00, 0x01, 0x02, 0x03]
    assert plaintext == expected
    assert len(plaintext) == len(ciphertext)

def test_invalid_key_length_raises():
    """Providing a key of invalid length should raise a ValueError."""
    bad_key = [0x00] * 15  # 15 bytes instead of 16/24/32
    ciphertext = CIPHERTEXT_BLOCK1
    with pytest.raises(ValueError):
        aes_cbc_decrypt(ciphertext, bad_key, IV)
