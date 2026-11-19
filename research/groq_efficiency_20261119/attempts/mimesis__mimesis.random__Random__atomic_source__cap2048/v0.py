import pytest
from mimesis.random import Random


def test_randints_normal_behavior():
    rng = Random()
    rng.seed(42)
    result = rng.randints(n=5, a=10, b=20)
    assert isinstance(result, list)
    assert len(result) == 5
    assert all(10 <= x < 20 for x in result)
    # deterministic seed should produce the same sequence
    rng2 = Random()
    rng2.seed(42)
    assert result == rng2.randints(n=5, a=10, b=20)


def test_randints_error_on_nonpositive_n():
    rng = Random()
    with pytest.raises(ValueError, match="n must be greater than 0"):
        rng.randints(n=0, a=1, b=10)
    with pytest.raises(ValueError, match="n must be greater than 0"):
        rng.randints(n=-3, a=1, b=10)


def test_generate_string_by_mask_and_placeholder_conflict():
    rng = Random()
    rng.seed(123)
    # Normal mask usage
    code = rng.generate_string_by_mask(mask="@@##", char="@")
    assert len(code) == 4
    assert code[0].isupper() and code[1].isupper()
    assert code[2].isdigit() and code[3].isdigit()
    # Placeholder conflict should raise ValueError
    with pytest.raises(ValueError, match="The same placeholder"):
        rng.generate_string_by_mask(mask="@@##", char="#", digit="#")
