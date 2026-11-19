import base64
import pytest
from youtube_dl.aes import (
    aes_decrypt_text,
    aes_encrypt,
    key_expansion,
    xor,
    BLOCK_SIZE_BYTES,
    inc,
    aes_ctr_decrypt,
)

def _build_ciphertext(plaintext_bytes, password, key_size_bytes):
    """Encrypt plaintext using the same algorithm as aes_decrypt_text."""
    # Prepare key
    password_bytes = password.encode("utf-8")
    key = list(password_bytes[:key_size_bytes]) + [0] * (key_size_bytes - len(password_bytes))
    key = aes_encrypt(key[:BLOCK_SIZE_BYTES], key_expansion(key)) * (key_size_bytes // BLOCK_SIZE_BYTES)

    # Nonce: 8 zero bytes
    nonce = [0] * 8
    # Counter object
    class Counter:
        __value = nonce + [0] * (BLOCK_SIZE_BYTES - len(nonce))

        def next_value(self):
            temp = self.__value
            self.__value = inc(self.__value)
            return temp

    # Pad plaintext to block size
    padded = list(plaintext_bytes) + [0] * (BLOCK_SIZE_BYTES - len(plaintext_bytes) % BLOCK_SIZE_BYTES)
    # Encrypt using counter mode
    cipher = aes_ctr_decrypt(padded, key, Counter())
    # Truncate to original length
    cipher = cipher[: len(plaintext_bytes)]
    # Prepend nonce
    data = nonce + cipher
    return base64.b64encode(bytes(data)).decode("ascii")

def test_aes_decrypt_text_roundtrip():
    plaintext = b"hello world!"
    password = "secret"
    key_size_bytes = 16
    data_b64 = _build_ciphertext(plaintext, password, key_size_bytes)
    decrypted = aes_decrypt_text(data_b64, password, key_size_bytes)
    assert decrypted == plaintext

def test_aes_decrypt_text_with_non_multiple_of_block():
    plaintext = b"1234567890"  # 10 bytes, not multiple of 16
    password = "pwd"
    key_size_bytes = 16
    data_b64 = _build_ciphertext(plaintext, password, key_size_bytes)
    decrypted = aes_decrypt_text(data_b64, password, key_size_bytes)
    assert decrypted == plaintext

def test_aes_decrypt_text_invalid_key_size():
    plaintext = b"test"
    password = "pass"
    key_size_bytes = 20  # invalid key size
    data_b64 = _build_ciphertext(plaintext, password, 16)  # build with valid key
    with pytest.raises(IndexError):
        aes_decrypt_text(data_b64, password, key_size_bytes)
