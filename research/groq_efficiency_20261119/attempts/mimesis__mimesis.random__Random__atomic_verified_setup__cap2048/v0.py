import pytest
from mimesis.random import Random


def test_randints_generates_correct_range_and_length():
    rng = Random()
    # Use a fixed seed for reproducibility
    rng.seed(42)
    result = rng.randints(n=5, a=10, b=20)
    assert isinstance(result, list)
    assert len(result) == 5
    # All values should be within [10, 19] inclusive
    assert all(10 <= x < 20 for x in result)


def test_generate_string_by_mask_raises_on_same_placeholder():
    rng = Random()
    # Using the same character for both placeholders should raise ValueError
    with pytest.raises(ValueError, match="The same placeholder cannot be used"):
        rng.generate_string_by_mask(mask="@@##", char="@")  # digit placeholder omitted


def test_weighted_choice_raises_on_empty_dict():
    rng = Random()
    with pytest.raises(ValueError, match="Choices cannot be empty"):
        rng.weighted_choice({})
