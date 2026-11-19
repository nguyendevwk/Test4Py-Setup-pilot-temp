import base64
import pytest
from youtube_dl.aes import aes_decrypt_text, BLOCK_SIZE_BYTES, aes_encrypt, key_expansion, inc, aes_ctr_decrypt

def test_decrypt_empty_cipher_returns_empty_bytes():
    # nonce of 8 zero bytes, no cipher
    nonce = b'\x00' * 8
    data_b64 = base64.b64encode(nonce).decode('ascii')
    password = "secret"
    key_size_bytes = 16  # 128‑bit key
    result = aes_decrypt_text(data_b64, password, key_size_bytes)
    assert result == b''

def test_decrypt_invalid_base64_raises():
    # data is not valid base64
    data_b64 = "!!!invalid!!!"
    password = "secret"
    key_size_bytes = 16
    with pytest.raises(Exception):
        aes_decrypt_text(data_b64, password, key_size_bytes)

def test_decrypt_with_short_password_and_nonempty_cipher():
    # Construct a simple cipher by encrypting a known plaintext using the same key derivation
    plaintext = b'hello world'
    password = "short"
    key_size_bytes = 16

    # Derive key as in aes_decrypt_text
    pwd_bytes = password.encode('utf-8')
    key = list(pwd_bytes[:key_size_bytes]) + [0] * (key_size_bytes - len(pwd_bytes))
    key = aes_encrypt(key[:BLOCK_SIZE_BYTES], key_expansion(key)) * (key_size_bytes // BLOCK_SIZE_BYTES)

    # Create counter starting from 8 zero bytes nonce
    nonce = [0] * 8
    class Counter(object):
        __value = nonce + [0] * (BLOCK_SIZE_BYTES - len(nonce))
        def next_value(self):
            temp = self.__value
            self.__value = inc(self.__value)
            return temp
    counter = Counter()

    # Encrypt plaintext using CTR mode (by XOR with keystream)
    cipher = aes_ctr_decrypt(list(plaintext), key, counter)  # same as decrypt because CTR is symmetric

    # Build data: nonce + cipher, base64 encode
    data_bytes = bytes(nonce + cipher)
    data_b64 = base64.b64encode(data_bytes).decode('ascii')

    # Decrypt using the function under test
    result = aes_decrypt_text(data_b64, password, key_size_bytes)
    assert result == plaintext
