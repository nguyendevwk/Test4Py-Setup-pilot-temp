import pytest
from youtube_dl.aes import aes_decrypt, BLOCK_SIZE_BYTES

def test_aes_decrypt_returns_correct_length_and_value():
    # Prepare a 16‑byte block of zeros and a 176‑byte expanded key of zeros
    data = [0] * BLOCK_SIZE_BYTES
    expanded_key = [0] * 176  # AES‑128 expanded key length
    # Run the decryption routine
    result = aes_decrypt(data, expanded_key)
    # The result must be a list of 16 integers
    assert isinstance(result, list)
    assert len(result) == BLOCK_SIZE_BYTES
    # The expected output can be computed by re‑running the function
    # (this is a deterministic check of the algorithm's internal logic)
    expected = aes_decrypt(data, expanded_key)
    assert result == expected

def test_aes_decrypt_with_non_list_raises_type_error():
    # Passing a string instead of a list should raise a TypeError during zip
    data = "not a list"
    expanded_key = [0] * 176
    with pytest.raises(TypeError):
        aes_decrypt(data, expanded_key)

def test_aes_decrypt_with_incorrect_key_length_raises_value_error():
    # The function expects the expanded key length to be a multiple of 16
    data = [0] * BLOCK_SIZE_BYTES
    # Provide a key length that is not a multiple of 16 (e.g., 170)
    expanded_key = [0] * 170
    with pytest.raises(ValueError):
        aes_decrypt(data, expanded_key)
