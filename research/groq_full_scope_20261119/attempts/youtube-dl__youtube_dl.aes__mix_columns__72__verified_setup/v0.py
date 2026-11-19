import pytest
from youtube_dl.aes import mix_columns

# Known AES mix_columns example from the FIPS-197 standard
# Input block (in hex): db 13 53 45
# Expected output block (in hex): 8e 4d a1 bc
INPUT_BLOCK = [0xdb, 0x13, 0x53, 0x45]
EXPECTED_OUTPUT = [0x8e, 0x4d, 0xa1, 0xbc]

def test_mix_columns_known_example():
    """Verify that mix_columns produces the expected result for a known input."""
    result = mix_columns(INPUT_BLOCK)
    assert result == EXPECTED_OUTPUT, f"Expected {EXPECTED_OUTPUT}, got {result}"

def test_mix_columns_multiple_of_four():
    """Ensure that mix_columns correctly processes a block of length 8 (two columns)."""
    # Two columns: first is the known example, second is all zeros
    input_block = INPUT_BLOCK + [0x00, 0x00, 0x00, 0x00]
    # Expected output: first column mixed, second column remains zeros
    expected = EXPECTED_OUTPUT + [0x00, 0x00, 0x00, 0x00]
    result = mix_columns(input_block)
    assert result == expected, f"Expected {expected}, got {result}"
    assert len(result) == 8, f"Result length should be 8, got {len(result)}"

def test_mix_columns_deterministic():
    """Check that mix_columns is deterministic: same input yields same output."""
    input_block = [0x01, 0x02, 0x03, 0x04,
                   0x05, 0x06, 0x07, 0x08]
    first_run = mix_columns(input_block)
    second_run = mix_columns(input_block)
    assert first_run == second_run, "mix_columns should produce identical results for identical inputs"
    # Ensure that the output is not the same object (i.e., a new list is returned)
    assert first_run is not second_run, "mix_columns should return a new list each call"
