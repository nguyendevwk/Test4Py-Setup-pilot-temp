import base64
import pytest
from youtube_dl.aes import (
    aes_encrypt,
    aes_ctr_decrypt,
    aes_decrypt_text,
    aes_encrypt_text,  # helper to create encrypted data
    BLOCK_SIZE_BYTES,
    key_expansion,
    inc,
    intlist_to_bytes,
    bytes_to_intlist,
    compat_b64decode,
)

# Helper to encrypt plaintext using the same logic as aes_decrypt_text
def _encrypt_plaintext(plaintext: bytes, password: str, key_size_bytes: int) -> str:
    # Build key
    key = bytes_to_intlist(password.encode("utf-8"))[:key_size_bytes]
    key += [0] * (key_size_bytes - len(key))
    key = aes_encrypt(key[:BLOCK_SIZE_BYTES], key_expansion(key)) * (key_size_bytes // BLOCK_SIZE_BYTES)

    # Counter nonce
    nonce = [0] * 8  # zero nonce for deterministic output
    counter = lambda: nonce + [0] * (BLOCK_SIZE_BYTES - len(nonce))

    # Encrypt
    cipher = aes_ctr_decrypt(bytes_to_intlist(plaintext), key, type("C", (), {"next_value": lambda self: counter()})())
    # Prepend nonce
    data_ints = nonce + cipher
    return base64.b64encode(intlist_to_bytes(data_ints)).decode("ascii")

def test_aes_decrypt_text_basic():
    """Decrypt a known plaintext encrypted with the same algorithm."""
    plaintext = b"Hello, world!"
    password = "secret"
    key_size_bytes = 16

    # Encrypt using helper
    encrypted_b64 = _encrypt_plaintext(plaintext, password, key_size_bytes)

    # Decrypt
    decrypted = aes_decrypt_text(encrypted_b64, password, key_size_bytes)

    assert decrypted == plaintext

def test_aes_decrypt_text_empty_plaintext():
    """Decrypt an empty plaintext; should return empty bytes."""
    plaintext = b""
    password = "empty"
    key_size_bytes = 16

    encrypted_b64 = _encrypt_plaintext(plaintext, password, key_size_bytes)
    decrypted = aes_decrypt_text(encrypted_b64, password, key_size_bytes)

    assert decrypted == plaintext
    assert isinstance(decrypted, bytes)

def test_aes_decrypt_text_invalid_base64():
    """Providing invalid base64 data should raise a binascii.Error."""
    invalid_b64 = "!!!not_base64!!!"
    password = "any"
    key_size_bytes = 16

    with pytest.raises(Exception) as excinfo:
        aes_decrypt_text(invalid_b64, password, key_size_bytes)
    # The underlying error is a binascii.Error, but we accept any exception
    assert "binascii" in str(excinfo.value).lower()
