import pytest
from mimesis.random import Random
from collections import Counter

# Test 1: Normal behavior of randints
def test_randints_normal():
    rnd = Random(seed=12345)
    result = rnd.randints(n=5, a=10, b=20)
    assert isinstance(result, list)
    assert len(result) == 5
    for value in result:
        assert 10 <= value <= 19  # inclusive lower, exclusive upper due to implementation

# Test 2: Error handling in generate_string_by_mask
def test_generate_string_by_mask_error():
    rnd = Random(seed=9876)
    # Using same placeholder for char and digit should raise ValueError
    with pytest.raises(ValueError, match="The same placeholder cannot be used for both numbers and characters."):
        rnd.generate_string_by_mask(mask="@#", char="@#", digit="@#")

# Test 3: Weighted choice distribution
def test_weighted_choice_distribution():
    rnd = Random(seed=555)
    choices = {"a": 1, "b": 2, "c": 3}
    # Draw many samples to approximate distribution
    samples = [rnd.weighted_choice(choices) for _ in range(6000)]
    counts = Counter(samples)
    # Expected proportions: a:1/6, b:2/6, c:3/6
    assert abs(counts["a"] / 6000 - 1/6) < 0.05
    assert abs(counts["b"] / 6000 - 2/6) < 0.05
    assert abs(counts["c"] / 6000 - 3/6) < 0.05
