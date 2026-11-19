import base64
import pytest
from youtube_dl.aes import (
    aes_encrypt,
    key_expansion,
    aes_ctr_encrypt,
    aes_ctr_decrypt,
    inc,
    BLOCK_SIZE_BYTES,
    bytes_to_intlist,
    intlist_to_bytes,
    aes_decrypt_text,
)

# Helper to create a ciphertext for a given plaintext and password
def _create_ciphertext(plaintext: bytes, password: str, key_size_bytes: int) -> str:
    # Encode plaintext to int list
    plaintext_ints = bytes_to_intlist(plaintext)

    # Create nonce (8 bytes) and counter
    nonce = [0] * 8  # simple zero nonce for deterministic test
    counter = nonce + [0] * (BLOCK_SIZE_BYTES - len(nonce))

    # Build key
    pwd_ints = bytes_to_intlist(password.encode("utf-8"))
    key = pwd_ints[:key_size_bytes] + [0] * (key_size_bytes - len(pwd_ints))
    key = aes_encrypt(key[:BLOCK_SIZE_BYTES], key_expansion(key)) * (key_size_bytes // BLOCK_SIZE_BYTES)

    # Encrypt
    cipher_ints = aes_ctr_encrypt(plaintext_ints, key, counter)

    # Prepend nonce and encode to base64
    data_ints = nonce + cipher_ints
    data_bytes = intlist_to_bytes(data_ints)
    return base64.b64encode(data_bytes).decode("ascii")

def test_aes_decrypt_text_basic():
    """Normal decryption with 128‑bit key and short password."""
    plaintext = b"Hello, world!"
    password = "secret"
    key_size_bytes = 16

    data_b64 = _create_ciphertext(plaintext, password, key_size_bytes)
    decrypted = aes_decrypt_text(data_b64, password, key_size_bytes)
    assert decrypted == plaintext

def test_aes_decrypt_text_long_password():
    """Decryption with a password longer than the key size (truncation)."""
    plaintext = b"Testing long password truncation."
    password = "this_is_a_very_long_password_exceeding_key_size"
    key_size_bytes = 16

    data_b64 = _create_ciphertext(plaintext, password, key_size_bytes)
    decrypted = aes_decrypt_text(data_b64, password, key_size_bytes)
    assert decrypted == plaintext

def test_aes_decrypt_text_boundary_key_size():
    """Decryption with maximum 256‑bit key size and zero‑padded password."""
    plaintext = b"Boundary key size test."
    password = "short"
    key_size_bytes = 32  # 256‑bit

    data_b64 = _create_ciphertext(plaintext, password, key_size_bytes)
    decrypted = aes_decrypt_text(data_b64, password, key_size_bytes)
    assert decrypted == plaintext
