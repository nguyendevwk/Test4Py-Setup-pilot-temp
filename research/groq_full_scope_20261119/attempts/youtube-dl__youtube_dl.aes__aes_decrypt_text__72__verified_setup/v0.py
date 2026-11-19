import base64
import pytest
from youtube_dl.aes import (
    aes_decrypt_text,
    aes_encrypt,
    key_expansion,
    aes_ctr_encrypt,
    BLOCK_SIZE_BYTES,
)

# Helper to create a ciphertext that can be decrypted by aes_decrypt_text
def create_ciphertext(plaintext: bytes, password: str, key_size_bytes: int) -> str:
    # Prepare key
    key = password.encode("utf-8")
    key = key[:key_size_bytes] + b"\x00" * (key_size_bytes - len(key))
    key = aes_encrypt(key[:BLOCK_SIZE_BYTES], key_expansion(key)) * (
        key_size_bytes // BLOCK_SIZE_BYTES
    )
    # Generate nonce
    nonce = b"12345678"  # 8 bytes nonce
    # Encrypt
    cipher = aes_ctr_encrypt(plaintext, key, nonce)
    # Prepend nonce and base64 encode
    return base64.b64encode(nonce + cipher).decode("ascii")


def test_aes_decrypt_text_roundtrip():
    plaintext = b"Hello, world! This is a test."
    password = "mysecretpassword"
    key_size_bytes = 16  # 128‑bit key
    data = create_ciphertext(plaintext, password, key_size_bytes)
    result = aes_decrypt_text(data, password, key_size_bytes)
    assert result == plaintext


def test_aes_decrypt_text_boundary_empty_plaintext():
    plaintext = b""
    password = "edgecase"
    key_size_bytes = 24  # 192‑bit key
    data = create_ciphertext(plaintext, password, key_size_bytes)
    result = aes_decrypt_text(data, password, key_size_bytes)
    assert result == plaintext


def test_aes_decrypt_text_invalid_key_size():
    plaintext = b"sample data"
    password = "short"
    key_size_bytes = 10  # invalid key size
    data = create_ciphertext(plaintext, password, 16)  # create with valid key size
    with pytest.raises(ValueError):
        aes_decrypt_text(data, password, key_size_bytes)
