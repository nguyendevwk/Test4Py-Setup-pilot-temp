import base64
import pytest
from youtube_dl.aes import aes_decrypt_text, aes_encrypt_text

def test_decrypt_returns_original_plaintext(tmp_path):
    # Prepare a small plaintext and password
    plaintext = b"Hello, world!"
    password = "secret"
    key_size_bytes = 16  # 128‑bit key

    # Encrypt the plaintext using the same library function
    encrypted_b64 = aes_encrypt_text(plaintext, password, key_size_bytes)

    # Decrypt the ciphertext
    decrypted = aes_decrypt_text(encrypted_b64, password, key_size_bytes)

    # The decrypted data should match the original plaintext
    assert decrypted == plaintext


def test_decrypt_with_wrong_key_size_returns_different_output(tmp_path):
    plaintext = b"Test data for key size mismatch."
    password = "another_secret"
    correct_key_size = 16
    wrong_key_size = 24

    # Encrypt with the correct key size
    encrypted_b64 = aes_encrypt_text(plaintext, password, correct_key_size)

    # Decrypt with a different key size
    decrypted_wrong = aes_decrypt_text(encrypted_b64, password, wrong_key_size)

    # The output should not match the original plaintext
    assert decrypted_wrong != plaintext
    # And it should not be empty
    assert decrypted_wrong


def test_decrypt_raises_on_invalid_base64_input():
    # Provide a string that is not valid base64
    invalid_b64 = "!!!not_base64!!!"
    password = "pwd"
    key_size_bytes = 16

    with pytest.raises(Exception):
        aes_decrypt_text(invalid_b64, password, key_size_bytes)
