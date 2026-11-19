import base64
import pytest

from youtube_dl.aes import aes_decrypt_text

def test_decrypt_empty_string_returns_empty_bytes():
    # Base64 of empty string is empty
    data = ""
    password = "any_password"
    key_size_bytes = 16
    result = aes_decrypt_text(data, password, key_size_bytes)
    assert result == b""


def test_password_shorter_than_key_size_is_padded_and_decrypts():
    # Use a password shorter than the key size; the function pads with zeros.
    # Encrypt a known plaintext using the same algorithm to produce a ciphertext.
    # Here we simply encrypt and then decrypt to verify round‑trip.
    from youtube_dl.aes import aes_encrypt, key_expansion, xor, BLOCK_SIZE_BYTES
    from youtube_dl.compat import compat_b64decode
    from youtube_dl.utils import bytes_to_intlist, intlist_to_bytes

    plaintext = b"Hello, AES!"
    # Pad plaintext to block size
    padded = plaintext + b"\x00" * (BLOCK_SIZE_BYTES - len(plaintext) % BLOCK_SIZE_BYTES)
    # Prepare key
    password = "short"
    key_size_bytes = 16
    key = bytes_to_intlist(password.encode("utf-8"))[:key_size_bytes] + [0] * (key_size_bytes - len(password))
    key = aes_encrypt(key[:BLOCK_SIZE_BYTES], key_expansion(key)) * (key_size_bytes // BLOCK_SIZE_BYTES)

    # Encrypt using counter mode
    from youtube_dl.aes import aes_ctr_decrypt
    class Counter:
        __value = [0] * BLOCK_SIZE_BYTES
        def next_value(self):
            return Counter.__value
    cipher = aes_ctr_decrypt(bytes_to_intlist(padded), key, Counter())
    # Encode to base64 for decryption function
    b64_cipher = base64.b64encode(intlist_to_bytes(cipher)).decode()
    # Decrypt
    decrypted = aes_decrypt_text(b64_cipher, password, key_size_bytes)
    assert decrypted == plaintext


def test_invalid_key_size_raises_index_error():
    data = base64.b64encode(b"test").decode()
    password = "password"
    key_size_bytes = 10  # invalid key size
    with pytest.raises(IndexError):
        aes_decrypt_text(data, password, key_size_bytes)
