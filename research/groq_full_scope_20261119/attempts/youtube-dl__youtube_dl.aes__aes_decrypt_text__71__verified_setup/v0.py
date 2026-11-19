import base64
import pytest
from youtube_dl.aes import (
    aes_encrypt_text,
    aes_decrypt_text,
    aes_encrypt,
    aes_ctr_encrypt,
    BLOCK_SIZE_BYTES,
    key_expansion,
    inc,
    aes_ctr_decrypt,
    intlist_to_bytes,
    bytes_to_intlist,
    compat_b64decode,
)

# Helper to create encrypted data in the format expected by aes_decrypt_text
def create_encrypted_data(plaintext: bytes, password: str, key_size_bytes: int) -> str:
    # Generate a nonce
    nonce = [0] * 8  # simple zero nonce for reproducibility
    # Encrypt plaintext
    cipher = aes_ctr_encrypt(bytes_to_intlist(plaintext), aes_encrypt(
        bytes_to_intlist(password.encode("utf-8"))[:BLOCK_SIZE_BYTES],
        key_expansion(bytes_to_intlist(password.encode("utf-8"))[:BLOCK_SIZE_BYTES]),
    ), nonce)
    # Combine nonce and cipher and base64 encode
    data_bytes = intlist_to_bytes(nonce + cipher)
    return base64.b64encode(data_bytes).decode("ascii")

def test_aes_decrypt_text_normal():
    plaintext = b"Hello, world!"
    password = "secret"
    key_size_bytes = 16
    data = create_encrypted_data(plaintext, password, key_size_bytes)
    result = aes_decrypt_text(data, password, key_size_bytes)
    assert result == plaintext

def test_aes_decrypt_text_empty_plaintext():
    plaintext = b""
    password = "empty"
    key_size_bytes = 16
    data = create_encrypted_data(plaintext, password, key_size_bytes)
    result = aes_decrypt_text(data, password, key_size_bytes)
    assert result == plaintext

def test_aes_decrypt_text_invalid_key_size():
    plaintext = b"Test data"
    password = "wrongsize"
    key_size_bytes = 20  # invalid key size
    data = create_encrypted_data(plaintext, password, 16)  # encrypt with valid size
    with pytest.raises(ValueError):
        aes_decrypt_text(data, password, key_size_bytes)
