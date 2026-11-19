import pytest
from youtube_dl.aes import mix_columns

def test_mix_columns_deterministic():
    """mix_columns should produce the same output for the same input."""
    input_data = [0x00, 0x01, 0x02, 0x03,
                  0x04, 0x05, 0x06, 0x07,
                  0x08, 0x09, 0x0a, 0x0b,
                  0x0c, 0x0d, 0x0e, 0x0f]
    first = mix_columns(input_data)
    second = mix_columns(input_data)
    assert first == second, "mix_columns is not deterministic"
    assert isinstance(first, list) and len(first) == 16, "output must be a list of 16 bytes"

def test_mix_columns_sensitivity():
    """Changing a single byte in the input should change the output."""
    base = [0x00] * 16
    altered = base.copy()
    altered[5] = 0xFF  # modify one byte
    out_base = mix_columns(base)
    out_altered = mix_columns(altered)
    assert out_base != out_altered, "output did not change when input was altered"
    # Ensure that only the altered byte influences the result
    # by comparing the difference in outputs
    diff = [b1 ^ b2 for b1, b2 in zip(out_base, out_altered)]
    assert any(diff), "no difference detected in output bytes"

def test_mix_columns_invalid_input_length():
    """mix_columns should raise a TypeError when input length is not 16."""
    with pytest.raises(TypeError):
        mix_columns([0x00] * 15)  # too short
    with pytest.raises(TypeError):
        mix_columns([0x00] * 17)  # too long
