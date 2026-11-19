import pytest
from mimesis.random import Random


def test_randints_and_uniform_behavior():
    rng = Random(seed=12345)
    # Normal case: generate 5 integers between 10 and 20
    ints = rng.randints(n=5, a=10, b=20)
    assert isinstance(ints, list)
    assert len(ints) == 5
    assert all(10 <= i < 20 for i in ints)

    # Uniform with precision: should be within [0, 1) and rounded to 3 decimals
    val = rng.uniform(0.0, 1.0, precision=3)
    assert 0.0 <= val < 1.0
    assert round(val, 3) == val


def test_generate_string_by_mask_and_error():
    rng = Random(seed=9876)
    # Normal mask: '@' -> letter, '#' -> digit
    code = rng.generate_string_by_mask(mask="@@##", char="@",
                                       digit="#")
    assert len(code) == 4
    assert code[:2].isalpha() and code[2:].isdigit()

    # Error when placeholders are identical
    with pytest.raises(ValueError, match="same placeholder"):
        rng.generate_string_by_mask(mask="@@##", char="@",
                                    digit="@")


def test_weighted_choice_and_randbytes():
    rng = Random(seed=5555)
    # Weighted choice: deterministic selection based on seed
    choices = {"a": 1, "b": 2, "c": 3}
    selected = rng.weighted_choice(choices)
    assert selected in choices

    # Error when choices dict is empty
    with pytest.raises(ValueError, match="empty"):
        rng.weighted_choice({})

    # Randbytes: check length and type
    data = rng.randbytes(8)
    assert isinstance(data, bytes)
    assert len(data) == 8
