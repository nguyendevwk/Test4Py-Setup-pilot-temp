import pytest
from youtube_dl.aes import aes_decrypt

def test_aes_decrypt_returns_list_of_length_16():
    # Use a dummy expanded key of 176 zero bytes (128‑bit AES)
    expanded_key = [0] * 176
    # Input data: 16 bytes of incremental values
    data = list(range(16))
    result = aes_decrypt(data, expanded_key)
    assert isinstance(result, list)
    assert len(result) == 16
    # With zero key and zeroed round keys, the output should equal the input
    assert result == data

def test_aes_decrypt_with_nonzero_key_changes_output():
    # Expanded key: first 16 bytes are 1, rest zeros
    expanded_key = [1] * 16 + [0] * (176 - 16)
    data = [0] * 16
    result = aes_decrypt(data, expanded_key)
    # The first round key XOR should change the data
    assert result[0] == 1
    # Remaining bytes should remain zero (since no other transformations affect them)
    assert result[1:] == [0] * 15

def test_aes_decrypt_raises_on_invalid_key_length():
    # Expanded key too short
    expanded_key = [0] * 10
    data = [0] * 16
    with pytest.raises(ZeroDivisionError):
        aes_decrypt(data, expanded_key)
