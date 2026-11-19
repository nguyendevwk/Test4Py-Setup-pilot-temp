import pytest
from youtube_dl.aes import aes_cbc_encrypt, key_expansion, aes_encrypt, xor, BLOCK_SIZE_BYTES

def test_aes_cbc_encrypt_basic_padding_and_length():
    # 3-byte cleartext, 16-byte zero key and IV
    data = [1, 2, 3]
    key = [0] * 16
    iv = [0] * 16

    encrypted = aes_cbc_encrypt(data, key, iv)

    # The output should be padded to the next multiple of BLOCK_SIZE_BYTES
    expected_len = ((len(data) + BLOCK_SIZE_BYTES - 1) // BLOCK_SIZE_BYTES) * BLOCK_SIZE_BYTES
    assert len(encrypted) == expected_len, "Encrypted data length mismatch"

    # The encrypted data should differ from the padded plaintext
    padded = data + [BLOCK_SIZE_BYTES - len(data)] * (BLOCK_SIZE_BYTES - len(data))
    assert encrypted != padded, "Encryption did not change the data"

def test_aes_cbc_encrypt_full_block_padding():
    # 16-byte cleartext, should add a full padding block of 16 bytes
    data = list(range(16))
    key = [0] * 16
    iv = [0] * 16

    encrypted = aes_cbc_encrypt(data, key, iv)

    # Two blocks: original + padding
    assert len(encrypted) == 32, "Encrypted data should be two blocks long"

    # The second block should be all 16s (PKCS#7 padding)
    second_block = encrypted[BLOCK_SIZE_BYTES:]
    assert all(byte == 16 for byte in second_block), "Padding block incorrect"

def test_aes_cbc_encrypt_invalid_key_length_raises():
    data = [1, 2, 3]
    iv = [0] * 16

    # Key lengths other than 16, 24, 32 should raise a ValueError
    for bad_len in (15, 17, 23, 25, 31, 33):
        key = [0] * bad_len
        with pytest.raises(ValueError):
            aes_cbc_encrypt(data, key, iv)
