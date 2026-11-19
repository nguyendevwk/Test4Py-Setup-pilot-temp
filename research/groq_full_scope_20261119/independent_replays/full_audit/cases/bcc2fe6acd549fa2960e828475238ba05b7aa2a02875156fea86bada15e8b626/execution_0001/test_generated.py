import pytest
from youtube_dl.aes import key_schedule_core, RCON

def test_key_schedule_core_returns_new_list_and_length():
    """key_schedule_core should return a new list of length 4."""
    data = [0x00, 0x01, 0x02, 0x03]
    result = key_schedule_core(data, 1)
    assert isinstance(result, list), "Result should be a list"
    assert len(result) == 4, "Result list should have length 4"

def test_key_schedule_core_does_not_modify_input():
    """The input list should remain unchanged after calling key_schedule_core."""
    data = [0x10, 0x20, 0x30, 0x40]
    data_copy = data.copy()
    key_schedule_core(data, 1)
    assert data == data_copy, "Input list should not be modified"

def test_key_schedule_core_invalid_rcon_raises_index_error():
    """Providing an out-of-range rcon_iteration should raise IndexError."""
    data = [0x00, 0x01, 0x02, 0x03]
    # RCON is a list; use an index larger than its length
    with pytest.raises(IndexError):
        key_schedule_core(data, len(RCON) + 10)
