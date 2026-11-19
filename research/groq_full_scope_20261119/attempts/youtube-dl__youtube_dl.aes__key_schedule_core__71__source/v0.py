import pytest
from youtube_dl.aes import key_schedule_core, RCON, rotate, sub_bytes

def test_key_schedule_core_changes_first_byte_based_on_rcon():
    # Input data: 4 bytes
    data = [0x01, 0x02, 0x03, 0x04]
    # Use two different rcon iterations
    out1 = key_schedule_core(data.copy(), 1)
    out2 = key_schedule_core(data.copy(), 2)

    # The first byte should differ because RCON[1] != RCON[2]
    assert out1[0] != out2[0], "First byte should change with different rcon_iteration"

    # The rest of the bytes should be the same because only the first byte is XORed with RCON
    assert out1[1:] == out2[1:], "Only the first byte should differ"

def test_key_schedule_core_applies_rotate_and_sub_bytes():
    # Input data: 4 bytes
    data = [0x00, 0x01, 0x02, 0x03]
    # Compute expected result manually
    rotated = rotate(data.copy())
    substituted = sub_bytes(rotated.copy())
    expected = substituted.copy()
    expected[0] ^= RCON[0]  # rcon_iteration 0

    result = key_schedule_core(data.copy(), 0)
    assert result == expected, "key_schedule_core should apply rotate, sub_bytes, and RCON XOR correctly"

def test_key_schedule_core_raises_type_error_on_invalid_input():
    # key_schedule_core expects a list of 4 integers
    with pytest.raises(TypeError):
        key_schedule_core("not a list", 0)
    with pytest.raises(TypeError):
        key_schedule_core([0x01, 0x02, 0x03], 0)  # too short
    with pytest.raises(TypeError):
        key_schedule_core([0x01, 0x02, 0x03, 0x04, 0x05], 0)  # too long
