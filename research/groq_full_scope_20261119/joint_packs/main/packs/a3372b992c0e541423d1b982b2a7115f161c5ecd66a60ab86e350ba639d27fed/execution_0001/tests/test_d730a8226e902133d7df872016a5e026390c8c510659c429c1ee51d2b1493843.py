import pytest
from youtube_dl.aes import key_schedule_core, RCON, rotate, sub_bytes

def test_key_schedule_core_returns_new_list_and_is_deterministic():
    # Input word (4 bytes)
    data = [0x2b, 0x28, 0xab, 0x09]
    # Make a copy to ensure original is not mutated
    original = data.copy()
    # Run the core twice with the same parameters
    out1 = key_schedule_core(data, 1)
    out2 = key_schedule_core(data, 1)
    # The output should be a new list each time
    assert out1 is not out2
    # The output should be deterministic
    assert out1 == out2
    # The original input should remain unchanged
    assert data == original
    # The output length should be 4
    assert len(out1) == 4

def test_key_schedule_core_changes_with_rcon():
    data = [0x2b, 0x28, 0xab, 0x09]
    # Run with two different rcon iterations
    out_rcon1 = key_schedule_core(data, 1)
    out_rcon2 = key_schedule_core(data, 2)
    # The outputs should differ because the RCON value is different
    assert out_rcon1 != out_rcon2
    # Ensure that the only difference comes from the XOR with RCON
    # by comparing the first byte after rotation and substitution
    rotated = rotate(data)
    substituted = sub_bytes(rotated)
    assert out_rcon1[0] == substituted[0] ^ RCON[1]
    assert out_rcon2[0] == substituted[0] ^ RCON[2]

def test_key_schedule_core_invalid_rcon_raises():
    data = [0x2b, 0x28, 0xab, 0x09]
    # RCON is defined for indices 0..10; index 11 should raise IndexError
    with pytest.raises(IndexError):
        key_schedule_core(data, 11)
