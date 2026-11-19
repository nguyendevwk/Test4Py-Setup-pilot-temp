import pytest
from mimesis.random import Random


def test_randints_normal_behavior():
    rng = Random()
    rng.seed(42)
    result = rng.randints(n=5, a=10, b=20)
    # With seed 42, the sequence should be deterministic
    assert result == [14, 12, 13, 12, 13]
    # Ensure all values are within the specified range
    assert all(10 <= x <= 19 for x in result)
    # The length should match the requested number of elements
    assert len(result) == 5


def test_randints_invalid_n_raises_value_error():
    rng = Random()
    with pytest.raises(ValueError, match="n must be greater than 0"):
        rng.randints(n=0, a=1, b=10)
    with pytest.raises(ValueError, match="n must be greater than 0"):
        rng.randints(n=-3, a=1, b=10)


def test_generate_string_by_mask_custom_placeholders():
    rng = Random()
    rng.seed(123)
    mask = "@#@#"
    code = rng.generate_string_by_mask(mask=mask, char="@", digit="#")
    # The code should have the same length as the mask
    assert len(code) == len(mask)
    # Characters at '@' positions should be uppercase letters
    assert all('A' <= c <= 'Z' for c in code[0::2])
    # Digits at '#' positions should be numeric digits
    assert all('0' <= c <= '9' for c in code[1::2])
    # With seed 123, the generated code should be deterministic
    assert code == "Q4W2"
