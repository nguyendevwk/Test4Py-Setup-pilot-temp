import base64
import pytest
from youtube_dl.aes import aes_decrypt_text, aes_encrypt_text

# Helper to create encrypted data for testing
def create_encrypted(plaintext: bytes, password: str, key_size_bytes: int) -> str:
    """Encrypt plaintext using the module's aes_encrypt_text and return base64 string."""
    # aes_encrypt_text expects a string, so we decode plaintext to str using latin1 to preserve bytes
    return aes_encrypt_text(plaintext.decode("latin1"), password, key_size_bytes)

def test_aes_decrypt_text_roundtrip():
    """Verify that decrypting data produced by the module returns the original plaintext."""
    plaintext = b"Hello, world! 12345"
    password = "secret_password"
    key_size = 16  # 128‑bit key
    encrypted_b64 = create_encrypted(plaintext, password, key_size)
    decrypted = aes_decrypt_text(encrypted_b64, password, key_size)
    assert decrypted == plaintext

def test_aes_decrypt_text_invalid_base64():
    """Decrypting with malformed base64 should raise a binascii.Error."""
    bad_b64 = "!!!not_base64!!!"
    password = "any"
    key_size = 16
    with pytest.raises(Exception) as excinfo:
        aes_decrypt_text(bad_b64, password, key_size)
    # The exception should be a binascii.Error or its subclass
    assert excinfo.type.__name__ in ("Error", "binascii.Error")

def test_aes_decrypt_text_wrong_password():
    """Decrypting with an incorrect password should not yield the original plaintext."""
    plaintext = b"Sensitive data that must stay secret."
    correct_password = "correcthorsebatterystaple"
    wrong_password = "incorrectpassword"
    key_size = 24  # 192‑bit key
    encrypted_b64 = create_encrypted(plaintext, correct_password, key_size)
    decrypted_with_wrong = aes_decrypt_text(encrypted_b64, wrong_password, key_size)
    assert decrypted_with_wrong != plaintext
    # The decrypted data should still be a byte string of the same length
    assert isinstance(decrypted_with_wrong, bytes)
    assert len(decrypted_with_wrong) == len(plaintext)
