import pytest
from mimesis.random import Random

def test_randints_normal_and_boundary():
    rng = Random()
    # Normal case: generate 5 integers between 10 and 20
    result = rng.randints(n=5, a=10, b=20)
    assert isinstance(result, list)
    assert len(result) == 5
    assert all(10 <= x < 20 for x in result)

    # Boundary case: n <= 0 should raise ValueError
    with pytest.raises(ValueError, match="n must be greater than 0"):
        rng.randints(n=0, a=1, b=10)

def test_generate_string_by_mask_custom_placeholders():
    rng = Random()
    # Use distinct placeholders
    code = rng.generate_string_by_mask(mask="A@B#C", char="@", digit="#")
    assert len(code) == 6
    # Positions with placeholders should be replaced appropriately
    assert code[0] == "A"
    assert code[1].isalpha() and code[1].isupper()
    assert code[2] == "B"
    assert code[3].isdigit()
    assert code[4] == "C"
    assert code[5].isalpha() and code[5].isupper()

    # Same placeholder for char and digit should raise ValueError
    with pytest.raises(ValueError, match="The same placeholder"):
        rng.generate_string_by_mask(mask="@@##", char="@", digit="@")

def test_weighted_choice_and_choice_enum_item():
    rng = Random()
    # Weighted choice: ensure selection respects weights
    choices = {"a": 1, "b": 3, "c": 6}
    # Run many times to statistically confirm distribution
    results = [rng.weighted_choice(choices) for _ in range(1000)]
    # 'c' should appear most frequently
    assert results.count("c") > results.count("b") > results.count("a")

    # Empty choices should raise ValueError
    with pytest.raises(ValueError, match="Choices cannot be empty"):
        rng.weighted_choice({})

    # Enum choice: use a simple enum
    import enum
    class Color(enum.Enum):
        RED = 1
        GREEN = 2
        BLUE = 3
    enum_result = rng.choice_enum_item(Color)
    assert enum_result in Color
