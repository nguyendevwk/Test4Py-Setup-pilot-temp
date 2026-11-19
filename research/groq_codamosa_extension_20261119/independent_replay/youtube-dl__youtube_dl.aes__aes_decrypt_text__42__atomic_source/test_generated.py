import base64
import pytest
from youtube_dl.aes import aes_decrypt_text

# Helper to create base64 data with given nonce and cipher bytes
def make_b64(nonce: bytes, cipher: bytes) -> str:
    return base64.b64encode(nonce + cipher).decode("ascii")

def test_decrypt_empty_cipher_returns_empty_bytes():
    # nonce of 8 bytes, cipher empty
    nonce = b"\x00" * 8
    data_b64 = make_b64(nonce, b"")
    # password shorter than key size, key will be padded
    plaintext = aes_decrypt_text(data_b64, "short", 16)
    assert plaintext == b""  # no ciphertext -> empty plaintext

def test_key_padding_with_short_password():
    # nonce of 8 bytes, cipher empty
    nonce = b"\x01\x02\x03\x04\x05\x06\x07\x08"
    data_b64 = make_b64(nonce, b"")
    # password length 5, key_size_bytes 24 -> padded with zeros
    plaintext = aes_decrypt_text(data_b64, "abcde", 24)
    assert plaintext == b""  # still empty plaintext
    # Ensure no exception raised and function returns bytes

def test_invalid_base64_raises_error():
    # malformed base64 string
    bad_b64 = "!!!not_base64!!!"
    with pytest.raises(Exception):
        aes_decrypt_text(bad_b64, "password", 16)
