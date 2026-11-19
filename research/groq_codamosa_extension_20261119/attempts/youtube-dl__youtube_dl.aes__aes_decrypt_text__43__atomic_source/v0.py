import base64
import pytest
from youtube_dl.aes import aes_decrypt_text

def test_decrypt_empty_data_returns_empty_bytes(tmp_path):
    # Base64 of an empty string is an empty string
    data = ""
    password = "any_password"
    key_size_bytes = 16
    result = aes_decrypt_text(data, password, key_size_bytes)
    assert result == b"", "Decrypting empty data should return empty bytes"

def test_decrypt_invalid_base64_raises_error():
    # Provide a string that is not valid Base64
    data = "!!!invalid_base64!!!"
    password = "password"
    key_size_bytes = 16
    with pytest.raises(Exception):
        aes_decrypt_text(data, password, key_size_bytes)

def test_decrypt_returns_bytes_type_and_non_empty(tmp_path):
    # Create a simple plaintext, encrypt it manually using the same algorithm
    # to produce a valid ciphertext for decryption.
    # Here we use the fact that the counter mode with a zero key will
    # produce ciphertext equal to plaintext (since AES encrypt of zero key is identity).
    # Construct nonce and ciphertext manually.
    plaintext = b"hello world"
    nonce = b"\x00" * 8
    # For zero key, aes_encrypt will produce zero key, so ciphertext == plaintext
    # We encode nonce + plaintext as base64
    data_bytes = nonce + plaintext
    data_b64 = base64.b64encode(data_bytes).decode()
    password = "0" * 16  # key will be zeros
    key_size_bytes = 16
    result = aes_decrypt_text(data_b64, password, key_size_bytes)
    assert isinstance(result, bytes), "Result should be of type bytes"
    assert result == plaintext, "Decrypted plaintext should match original"
