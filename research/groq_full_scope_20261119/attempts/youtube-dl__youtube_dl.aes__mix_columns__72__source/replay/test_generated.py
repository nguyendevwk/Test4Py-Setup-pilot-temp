import pytest
from youtube_dl.aes import mix_columns

# Known AES mix_columns example (from the AES specification)
# Input block: 0xdb 0x13 0x53 0x45 0xf2 0x0a 0x22 0x5c 0x01 0x01 0x01 0x01 0x01 0x01 0x01 0x01
# After mix_columns on each column, the first column should become: 0x8e 0x4d 0xa1 0xbc
INPUT_BLOCK = [
    0xdb, 0x13, 0x53, 0x45,
    0xf2, 0x0a, 0x22, 0x5c,
    0x01, 0x01, 0x01, 0x01,
    0x01, 0x01, 0x01, 0x01,
]
EXPECTED_FIRST_COLUMN = [0x8e, 0x4d, 0xa1, 0xbc]

def test_mix_columns_known_example():
    """Verify that mix_columns transforms a known input to the expected output."""
    mixed = mix_columns(INPUT_BLOCK)
    # The function returns a flat list of 16 bytes
    assert len(mixed) == 16
    # Check that the first four bytes match the expected transformed column
    assert mixed[:4] == EXPECTED_FIRST_COLUMN

def test_mix_columns_length_and_type():
    """Ensure that mix_columns accepts a list of 16 integers and returns a list of the same length."""
    data = list(range(16))
    mixed = mix_columns(data)
    assert isinstance(mixed, list)
    assert len(mixed) == 16
    # The transformation should not produce any values outside the byte range
    assert all(0 <= b <= 255 for b in mixed)

def test_mix_columns_invalid_input():
    """mix_columns should raise a TypeError when the input is not a list of integers."""
    with pytest.raises(TypeError):
        mix_columns("not a list")
