import pytest
from youtube_dl.aes import key_schedule_core, RCON, SBOX

def test_key_schedule_core_normal():
    # Input data and rcon_iteration chosen arbitrarily
    data = [0x00, 0x01, 0x02, 0x03]
    rcon_iteration = 1
    # Expected result computed manually
    rotated = data[1:] + [data[0]]          # [0x01, 0x02, 0x03, 0x00]
    substituted = [SBOX[x] for x in rotated]  # apply SBOX
    substituted[0] ^= RCON[rcon_iteration]   # XOR with RCON[1] (0x01)
    expected = substituted
    result = key_schedule_core(data, rcon_iteration)
    assert result == expected, f"Expected {expected}, got {result}"

def test_key_schedule_core_rcon_out_of_bounds():
    data = [0x00, 0x01, 0x02, 0x03]
    # RCON has indices 0..10; index 11 should raise IndexError
    with pytest.raises(IndexError):
        key_schedule_core(data, 11)

def test_key_schedule_core_single_byte():
    # Test with a single-byte list; rotate and sub_bytes should still work
    data = [0x5a]
    rcon_iteration = 0
    rotated = data[1:] + [data[0]]          # same single element
    substituted = [SBOX[x] for x in rotated]
    substituted[0] ^= RCON[rcon_iteration]   # XOR with RCON[0] (0x8d)
    expected = substituted
    result = key_schedule_core(data, rcon_iteration)
    assert result == expected, f"Expected {expected}, got {result}"
