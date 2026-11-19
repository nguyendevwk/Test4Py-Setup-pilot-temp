import pytest
from youtube_dl.aes import aes_cbc_encrypt, BLOCK_SIZE_BYTES

def test_empty_input_returns_empty_output():
    """When data is empty, no blocks are processed and the result is an empty list."""
    data = []
    key = [0] * 16
    iv = [0] * 16
    result = aes_cbc_encrypt(data, key, iv)
    assert result == [], "Expected empty list for empty input data"

def test_padding_and_output_length():
    """
    Verify that the output length is a multiple of BLOCK_SIZE_BYTES and that
    the padding byte value equals the number of padding bytes added.
    """
    data = [1, 2, 3]  # 3 bytes of data
    key = [0] * 16
    iv = [0] * 16
    result = aes_cbc_encrypt(data, key, iv)

    # Output length must be a multiple of BLOCK_SIZE_BYTES
    assert len(result) % BLOCK_SIZE_BYTES == 0, "Output length not a multiple of block size"

    # The last byte of the output corresponds to the padding byte of the last block
    # Since we used a dummy key and iv, the padding byte will be the same as the
    # padding length added to the last block.
    padding_length = BLOCK_SIZE_BYTES - len(data)
    assert result[-1] == padding_length, (
        f"Expected padding byte {padding_length}, got {result[-1]}"
    )

def test_different_iv_changes_output():
    """
    The same data and key but different IVs should produce different ciphertexts.
    """
    data = [10] * 32  # two full blocks of data
    key = [0] * 16
    iv1 = [0] * 16
    iv2 = [1] * 16  # different IV

    out1 = aes_cbc_encrypt(data, key, iv1)
    out2 = aes_cbc_encrypt(data, key, iv2)

    assert out1 != out2, "Ciphertexts should differ when IV changes"
    assert len(out1) == len(out2), "Ciphertexts should have the same length"
