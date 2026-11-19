import pytest
from mimesis.random import Random


def test_randints_normal_and_range():
    rng = Random()
    # deterministic seed for reproducibility
    rng.seed(42)
    result = rng.randints(n=5, a=10, b=20)
    assert isinstance(result, list)
    assert len(result) == 5
    # All values should be within [10, 19]
    assert all(10 <= x < 20 for x in result)
    # Check that the values are integers
    assert all(isinstance(x, int) for x in result)


def test_randints_error_and_generate_string_by_mask_error():
    rng = Random()
    # randints should raise ValueError for non‑positive n
    with pytest.raises(ValueError, match="n must be greater than 0"):
        rng.randints(n=0, a=1, b=10)

    # generate_string_by_mask should raise ValueError when placeholders collide
    with pytest.raises(ValueError, match="The same placeholder cannot be used"):
        rng.generate_string_by_mask(mask="@@##", char="@")

    # weighted_choice should raise ValueError when choices dict is empty
    with pytest.raises(ValueError, match="Choices cannot be empty."):
        rng.weighted_choice({})


def test_generate_string_by_mask_output_and_uniform_precision():
    rng = Random()
    rng.seed(123)
    # Generate a string with a mix of characters and digits
    code = rng.generate_string_by_mask(mask="A@#B", char="@", digit="#")
    assert len(code) == 4
    # Positions: 0 and 3 are fixed letters, 1 is a random uppercase letter, 2 is a random digit
    assert code[0] == "A"
    assert code[3] == "B"
    assert code[1].isupper() and len(code[1]) == 1
    assert code[2].isdigit() and len(code[2]) == 1

    # Test uniform rounding precision
    val = rng.uniform(0.0, 1.0, precision=2)
    assert isinstance(val, float)
    # The value should be rounded to 2 decimal places
    assert round(val, 2) == val
