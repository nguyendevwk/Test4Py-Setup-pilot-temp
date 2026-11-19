import pytest
from youtube_dl.aes import aes_cbc_decrypt, BLOCK_SIZE_BYTES

# Test vector from NIST SP 800-38A
KEY = [
    0x2b, 0x7e, 0x15, 0x16,
    0x28, 0xae, 0xd2, 0xa6,
    0xab, 0xf7, 0x15, 0x88,
    0x09, 0xcf, 0x4f, 0x3c
]
PLAINTEXT = [
    0x6b, 0xc1, 0xbe, 0xe2,
    0x2e, 0x40, 0x9f, 0x96,
    0xe9, 0x3d, 0x7e, 0x11,
    0x73, 0x93, 0x17, 0x2a
]
CIPHERTEXT = [
    0x3a, 0xd7, 0x7b, 0xb4,
    0x0d, 0x7a, 0x36, 0x60,
    0xa8, 0x9e, 0xca, 0xf3,
    0x24, 0x66, 0xef, 0x97
]
IV = [0] * BLOCK_SIZE_BYTES

def test_aes_cbc_decrypt_known_vector():
    """Decrypt a single block with a known test vector."""
    decrypted = aes_cbc_decrypt(CIPHERTEXT, KEY, IV)
    assert decrypted == PLAINTEXT

def test_aes_cbc_decrypt_partial_block():
    """Decrypt data whose length is not a multiple of the block size."""
    # Append 4 extra bytes to the ciphertext to create a 20‑byte input
    data = CIPHERTEXT + [0x00, 0x01, 0x02, 0x03]
    decrypted = aes_cbc_decrypt(data, KEY, IV)
    # The function pads the last block with zeros, decrypts it, then truncates
    # to the original length (20 bytes). The first 16 bytes should match the
    # plaintext, the remaining 4 bytes are the result of decrypting the padded
    # block and then truncating.
    assert decrypted[:16] == PLAINTEXT
    assert len(decrypted) == 20

def test_aes_cbc_decrypt_empty_input():
    """Decrypting an empty input should return an empty list."""
    assert aes_cbc_decrypt([], KEY, IV) == []
