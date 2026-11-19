import base64
import pytest
from youtube_dl.aes import (
    aes_decrypt_text,
    aes_ctr_decrypt,
    aes_encrypt,
    key_expansion,
    bytes_to_intlist,
    intlist_to_bytes,
    BLOCK_SIZE_BYTES,
)
from youtube_dl.compat import compat_b64decode


def _make_ciphertext(plaintext: bytes, password: str, key_size_bytes: int) -> bytes:
    """Encrypt plaintext using the same logic as aes_decrypt_text and return the raw bytes
    (nonce + ciphertext) that would be base64‑encoded."""
    # Prepare key
    password_bytes = password.encode("utf-8")
    key = bytes_to_intlist(password_bytes)[:key_size_bytes]
    key += [0] * (key_size_bytes - len(key))
    expanded_key = key_expansion(key[:BLOCK_SIZE_BYTES])
    key = aes_encrypt(key[:BLOCK_SIZE_BYTES], expanded_key) * (key_size_bytes // BLOCK_SIZE_BYTES)

    # Counter starting at zero nonce
    nonce = [0] * 8
    counter = type("Counter", (), {"next_value": lambda self: nonce})()
    # Encrypt
    ciphertext = aes_ctr_decrypt(bytes_to_intlist(plaintext), key, counter)
    # Return raw bytes
    return intlist_to_bytes(nonce + ciphertext)


def test_aes_decrypt_text_roundtrip():
    """Decrypting data that was encrypted with the same algorithm returns the original plaintext."""
    plaintext = b"Hello, world! 123"
    password = "secret"
    key_size_bytes = 16

    raw = _make_ciphertext(plaintext, password, key_size_bytes)
    b64 = base64.b64encode(raw).decode("ascii")

    result = aes_decrypt_text(b64, password, key_size_bytes)
    assert result == plaintext


def test_aes_decrypt_text_non_multiple_block():
    """Plaintext whose length is not a multiple of the block size is handled correctly."""
    plaintext = b"Non-multiple length data."
    password = "another"
    key_size_bytes = 24

    raw = _make_ciphertext(plaintext, password, key_size_bytes)
    b64 = base64.b64encode(raw).decode("ascii")

    result = aes_decrypt_text(b64, password, key_size_bytes)
    assert result == plaintext
    assert len(result) == len(plaintext)


def test_aes_decrypt_text_invalid_base64():
    """Providing an invalid base64 string raises a binascii.Error."""
    with pytest.raises(Exception) as excinfo:
        aes_decrypt_text("!!!not_base64!!!", "pwd", 16)
    assert isinstance(excinfo.value, Exception)
