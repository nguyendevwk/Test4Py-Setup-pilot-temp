import pytest
from youtube_dl.aes import mix_columns, MIX_COLUMN_MATRIX

# Test 1: Verify that mix_columns produces the known AES mix‑columns result
def test_mix_columns_known_example():
    # Input state (16 bytes) from the AES specification example
    input_state = [
        0x87, 0xF2, 0x4D, 0x97,
        0x6E, 0x4C, 0x90, 0xEC,
        0x46, 0xE7, 0x4A, 0xC3,
        0xA6, 0x8C, 0xD8, 0x95
    ]
    # Expected output after mix_columns (same as AES spec)
    expected_output = [
        0x47, 0x58, 0x30, 0x8D,
        0x7E, 0x9A, 0xF7, 0xA4,
        0xF2, 0xF4, 0xD3, 0x7A,
        0xE3, 0x4C, 0xF8, 0x78
    ]
    result = mix_columns(input_state)
    assert result == expected_output, f"Expected {expected_output}, got {result}"

# Test 2: Verify that mix_columns with a custom matrix that is all ones
# produces the XOR of each column as each output byte
def test_mix_columns_identity_matrix():
    # Create a matrix where every element is 1
    identity_matrix = ((1, 1, 1, 1),
                       (1, 1, 1, 1),
                       (1, 1, 1, 1),
                       (1, 1, 1, 1))
    # Input state: 16 bytes with incremental values
    input_state = list(range(16))
    # For each column, the XOR of its four bytes should be the output
    expected = []
    for i in range(4):
        column = input_state[i*4:(i+1)*4]
        column_xor = 0
        for b in column:
            column_xor ^= b
        expected.extend([column_xor]*4)
    result = mix_columns(input_state, matrix=identity_matrix)
    assert result == expected, f"Expected {expected}, got {result}"

# Test 3: Verify that mix_columns correctly handles a state where all bytes are zero
def test_mix_columns_all_zero():
    zero_state = [0] * 16
    result = mix_columns(zero_state)
    assert result == [0] * 16, f"Expected all zeros, got {result}"
