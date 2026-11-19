import pytest
from youtube_dl.aes import aes_cbc_decrypt, BLOCK_SIZE_BYTES

# Test vector from NIST SP 800-38A: AES-128 ECB with zero key
# Plaintext: 16 bytes of 0x00..0x0f
# Ciphertext: 0x66e94bd4ef8a2c3b884cfa59ca342b2e
ZERO_KEY = [0x00] * 16
ZERO_IV = [0x00] * 16
PLAINTEXT = list(range(16))
CIPHERTEXT = [0x66, 0xe9, 0x4b, 0xd4, 0xef, 0x8a, 0x2c, 0x3b,
              0x88, 0x4c, 0xfa, 0x59, 0xca, 0x34, 0x2b, 0x2e]

def test_aes_cbc_decrypt_full_block():
    """Decrypt a single full block with zero key and IV."""
    decrypted = aes_cbc_decrypt(CIPHERTEXT, ZERO_KEY, ZERO_IV)
    assert decrypted == PLAINTEXT

def test_aes_cbc_decrypt_partial_block():
    """Decrypt data whose length is not a multiple of the block size."""
    # Use the same ciphertext but truncate to 10 bytes
    truncated_cipher = CIPHERTEXT[:10]
    decrypted = aes_cbc_decrypt(truncated_cipher, ZERO_KEY, ZERO_IV)
    # The first 10 bytes of the plaintext should be returned
    assert decrypted == PLAINTEXT[:10]
    # Length should match the input length
    assert len(decrypted) == 10

def test_aes_cbc_decrypt_empty_input():
    """Decrypting an empty list should return an empty list."""
    decrypted = aes_cbc_decrypt([], ZERO_KEY, ZERO_IV)
    assert decrypted == []
    assert isinstance(decrypted, list)
