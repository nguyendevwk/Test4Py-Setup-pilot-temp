import pytest
from mimesis.random import Random


def test_randints_normal_behavior():
    rnd = Random()
    # deterministic seed for reproducibility
    rnd.seed(42)
    result = rnd.randints(n=5, a=10, b=20)
    assert isinstance(result, list)
    assert len(result) == 5
    # All values should be within [10, 19]
    assert all(10 <= x < 20 for x in result)
    # With the same seed, the sequence should be repeatable
    rnd2 = Random()
    rnd2.seed(42)
    assert rnd2.randints(n=5, a=10, b=20) == result


def test_generate_string_by_mask_success_and_error():
    rnd = Random()
    rnd.seed(123)
    # Normal mask with distinct placeholders
    code = rnd.generate_string_by_mask(mask="@@##", char="@")
    assert len(code) == 4
    # First two should be uppercase letters, last two digits
    assert code[:2].isupper()
    assert code[2:].isdigit()

    # Error when placeholders are the same
    with pytest.raises(ValueError, match="same placeholder"):
        rnd.generate_string_by_mask(mask="@@##", char="#", digit="#")


def test_weighted_choice_error_and_distribution():
    rnd = Random()
    rnd.seed(7)
    # Empty choices should raise ValueError
    with pytest.raises(ValueError, match="empty"):
        rnd.weighted_choice({})

    # Test that weighted_choice respects weights
    choices = {"a": 1, "b": 3, "c": 6}
    # Run many times to approximate distribution
    results = [rnd.weighted_choice(choices) for _ in range(1000)]
    # 'c' should appear roughly 60% of the time
    assert 500 < results.count("c") < 700
    # 'a' should appear roughly 10% of the time
    assert 80 < results.count("a") < 120
