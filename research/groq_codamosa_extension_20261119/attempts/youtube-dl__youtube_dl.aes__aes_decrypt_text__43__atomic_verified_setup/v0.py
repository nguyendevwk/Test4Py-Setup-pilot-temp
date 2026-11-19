import base64
import pytest
from youtube_dl.aes import aes_decrypt_text

def test_aes_decrypt_text_invalid_base64():
    """Passing non‑base64 data should raise a binascii.Error."""
    with pytest.raises(Exception) as excinfo:
        aes_decrypt_text("not_base64!", "password", 16)
    # The exception should be a binascii.Error or its subclass
    assert excinfo.type.__name__ in ("Error", "binascii.Error", "binascii.Error")

def test_aes_decrypt_text_returns_bytes():
    """The function should return a bytes object."""
    # Create a minimal valid base64 string: 8 nonce bytes + 16 cipher bytes
    nonce = b'\x00' * 8
    cipher = b'\x00' * 16
    data = base64.b64encode(nonce + cipher).decode('ascii')
    result = aes_decrypt_text(data, "pass", 16)
    assert isinstance(result, bytes)
    # With all-zero key and counter, the keystream is all zeros, so plaintext is all zeros
    assert result == b'\x00' * 16

def test_aes_decrypt_text_password_padding():
    """Password shorter than key_size_bytes should be padded with zeros."""
    # Use a password of length 5, key_size_bytes=16
    nonce = b'\x00' * 8
    cipher = b'\x00' * 16
    data = base64.b64encode(nonce + cipher).decode('ascii')
    result = aes_decrypt_text(data, "abcde", 16)
    assert isinstance(result, bytes)
    assert result == b'\x00' * 16
