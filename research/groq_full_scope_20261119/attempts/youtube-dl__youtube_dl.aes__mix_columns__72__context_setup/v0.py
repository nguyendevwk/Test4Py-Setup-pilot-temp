import pytest
from youtube_dl.aes import mix_columns, MIX_COLUMN_MATRIX

# Test 1: Known AES mix column example from the specification
def test_mix_columns_known_example():
    # Input column from the AES spec: [0x87, 0xF2, 0x4D, 0x97]
    # Expected output after mix_columns: [0x47, 0x58, 0xA6, 0x5B]
    input_state = [0x87, 0xF2, 0x4D, 0x97] * 4  # repeat to form a 16‑byte state
    expected_state = [0x47, 0x58, 0xA6, 0x5B] * 4
    result = mix_columns(input_state, MIX_COLUMN_MATRIX)
    assert result == expected_state

# Test 2: Boundary case – all zero input should produce all zero output
def test_mix_columns_all_zero():
    zero_state = [0x00] * 16
    result = mix_columns(zero_state, MIX_COLUMN_MATRIX)
    assert result == zero_state

# Test 3: Error handling – passing non‑integer data should raise a TypeError
def test_mix_columns_invalid_input_type():
    invalid_state = ['a', 'b', 'c', 'd'] * 4
    with pytest.raises(TypeError):
        mix_columns(invalid_state, MIX_COLUMN_MATRIX)
