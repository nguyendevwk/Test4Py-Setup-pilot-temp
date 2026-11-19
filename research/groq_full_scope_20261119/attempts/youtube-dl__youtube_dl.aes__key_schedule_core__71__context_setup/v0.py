import pytest
from youtube_dl.aes import key_schedule_core, RCON, SBOX

def test_key_schedule_core_normal():
    # Example from the AES specification
    input_word = [0x2b, 0x28, 0xab, 0x09]
    expected_output = [0x8e, 0x4d, 0xa1, 0xbc]
    assert key_schedule_core(input_word, 1) == expected_output

def test_key_schedule_core_boundary():
    # rcon_iteration 0 uses RCON[0] = 0x8d
    input_word = [0x00, 0x00, 0x00, 0x00]
    # rotate -> [0,0,0,0]; sub_bytes -> [0x63,0x63,0x63,0x63]
    # XOR first element with 0x8d: 0x63 ^ 0x8d = 0xee
    expected_output = [0xee, 0x63, 0x63, 0x63]
    assert key_schedule_core(input_word, 0) == expected_output

def test_key_schedule_core_invalid_input():
    # Passing a non-iterable should raise a TypeError
    with pytest.raises(TypeError):
        key_schedule_core(None, 1)
