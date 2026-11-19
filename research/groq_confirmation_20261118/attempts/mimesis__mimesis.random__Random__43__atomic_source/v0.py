import pytest
from mimesis.random import Random


def test_randints_normal_and_boundary():
    rng = Random(42)
    # Normal case: generate 5 integers between 10 and 20
    result = rng.randints(n=5, a=10, b=20)
    assert isinstance(result, list)
    assert len(result) == 5
    assert all(10 <= x < 20 for x in result)

    # Boundary case: n <= 0 should raise ValueError
    with pytest.raises(ValueError, match="n must be greater than 0"):
        rng.randints(n=0, a=1, b=10)


def test_generate_string_by_mask_custom_placeholders():
    rng = Random(123)
    # Use custom placeholders: '$' for letters, '%' for digits
    mask = "$%$%$"
    result = rng.generate_string_by_mask(mask=mask, char="$", digit="%")
    # Result should match the mask pattern
    assert len(result) == len(mask)
    for i, ch in enumerate(mask):
        if ch == "$":
            assert result[i].isalpha() and result[i].isupper()
        elif ch == "%":
            assert result[i].isdigit()
        else:
            assert result[i] == ch

    # Same placeholder for both should raise ValueError
    with pytest.raises(ValueError, match="The same placeholder"):
        rng.generate_string_by_mask(mask="@@@", char="@")  # digit default '#', but char same as placeholder


def test_weighted_choice_distribution_and_error():
    rng = Random(999)
    # Weighted choice with deterministic seed should always pick the same key
    choices = {"a": 1, "b": 2, "c": 3}
    first_choice = rng.weighted_choice(choices)
    second_choice = rng.weighted_choice(choices)
    assert first_choice == second_choice
    assert first_choice in choices

    # Empty choices should raise ValueError
    with pytest.raises(ValueError, match="Choices cannot be empty"):
        rng.weighted_choice({})
