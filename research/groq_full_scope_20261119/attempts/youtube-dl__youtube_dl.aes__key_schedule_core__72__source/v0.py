import pytest
from youtube_dl.aes import key_schedule_core, RCON

def test_key_schedule_core_basic():
    # Known input and expected output for rcon_iteration = 1
    data = [0x00, 0x01, 0x02, 0x03]
    expected = [0x7d, 0x77, 0x7b, 0x63]  # computed manually using AES S-box and RCON[1] = 0x01
    result = key_schedule_core(data, 1)
    assert result == expected
    # Ensure the original data is unchanged
    assert data == [0x00, 0x01, 0x02, 0x03]

def test_key_schedule_core_new_object():
    data = [0x10, 0x20, 0x30, 0x40]
    result = key_schedule_core(data, 2)
    # The returned list should be a new object, not the same reference
    assert result is not data
    # The content should differ from the input
    assert result != data

def test_key_schedule_core_invalid_rcon():
    data = [0x00, 0x01, 0x02, 0x03]
    # RCON has a finite length; using an index beyond its bounds should raise IndexError
    with pytest.raises(IndexError):
        key_schedule_core(data, len(RCON) + 1)
