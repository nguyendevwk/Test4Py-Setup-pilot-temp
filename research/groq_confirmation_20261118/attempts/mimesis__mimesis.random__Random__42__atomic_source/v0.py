import pytest
from mimesis.random import Random


def test_randints_normal_behavior():
    rnd = Random()
    # Seed to make deterministic
    rnd.seed(42)
    result = rnd.randints(n=5, a=10, b=20)
    # With seed 42, the first 5 random floats are known; check that the list
    # contains 5 integers within the specified range and that they are not all equal.
    assert isinstance(result, list)
    assert len(result) == 5
    assert all(10 <= x <= 19 for x in result)
    assert len(set(result)) > 1  # ensure randomness


def test_generate_string_by_mask_error_same_placeholder():
    rnd = Random()
    # Using the same placeholder for both char and digit should raise ValueError
    with pytest.raises(ValueError, match="The same placeholder"):
        rnd.generate_string_by_mask(mask="@@##", char="@")
    # Ensure that the error message is specific
    with pytest.raises(ValueError, match="cannot be used for both"):
        rnd.generate_string_by_mask(mask="@@##", char="@", digit="@")


def test_weighted_choice_empty_and_single_choice():
    rnd = Random()
    rnd.seed(123)
    # Empty dict should raise ValueError
    with pytest.raises(ValueError, match="cannot be empty"):
        rnd.weighted_choice({})
    # Single choice should always return that key
    single = {"only": 1.0}
    assert rnd.weighted_choice(single) == "only"
    # Multiple choices: verify that the returned value is one of the keys
    choices = {"a": 1.0, "b": 2.0, "c": 3.0}
    result = rnd.weighted_choice(choices)
    assert result in choices
