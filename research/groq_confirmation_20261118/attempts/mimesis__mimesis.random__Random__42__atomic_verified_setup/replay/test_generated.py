import pytest
from mimesis.random import Random


def test_randints_generates_correct_range_and_length():
    rng = Random()
    # Seed to make deterministic
    rng.seed(42)
    result = rng.randints(n=5, a=10, b=20)
    assert isinstance(result, list)
    assert len(result) == 5
    # All values should be within [10, 20)
    assert all(10 <= x < 20 for x in result)
    # With the same seed, the sequence should repeat
    rng2 = Random()
    rng2.seed(42)
    assert rng2.randints(n=5, a=10, b=20) == result


def test_generate_string_by_mask_uses_placeholders_and_randomness():
    rng = Random()
    rng.seed(123)
    mask = "@#@#"
    code = rng.generate_string_by_mask(mask=mask, char="@", digit="#")
    # Code should have same length as mask
    assert len(code) == len(mask)
    # Characters at '@' positions should be uppercase letters
    for i, ch in enumerate(mask):
        if ch == "@":
            assert code[i].isupper() and code[i].isalpha()
        elif ch == "#":
            assert code[i].isdigit()
        else:
            assert code[i] == ch
    # With same seed, same code should be produced
    rng2 = Random()
    rng2.seed(123)
    assert rng2.generate_string_by_mask(mask=mask, char="@", digit="#") == code


def test_weighted_choice_raises_on_empty_and_returns_valid_key():
    rng = Random()
    rng.seed(999)
    # Empty dict should raise ValueError
    with pytest.raises(ValueError, match="Choices cannot be empty"):
        rng.weighted_choice({})
    # Non-empty dict should return a key from the dict
    choices = {"a": 1.0, "b": 2.0, "c": 3.0}
    result = rng.weighted_choice(choices)
    assert result in choices
    # With same seed, the result should be deterministic
    rng2 = Random()
    rng2.seed(999)
    assert rng2.weighted_choice(choices) == result
