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
    # Use default mask "@###" with distinct placeholders
    code = rng.generate_string_by_mask()
    assert len(code) == 4
    # First character should be uppercase letter
    assert code[0].isupper()
    # Remaining three should be digits
    assert all(ch.isdigit() for ch in code[1:])

    # Test that using same placeholder for char and digit raises ValueError
    with pytest.raises(ValueError, match="The same placeholder cannot be used for both numbers and characters."):
        rng.generate_string_by_mask(mask="@@@", char="#", digit="#")


def test_weighted_choice_and_choice_enum_item():
    rng = Random()
    # Weighted choice: ensure selection follows weights
    choices = {"a": 1, "b": 2, "c": 3}
    # Run many times to statistically confirm distribution
    results = [rng.weighted_choice(choices) for _ in range(1000)]
    assert all(item in choices for item in results)
    # 'c' should appear more often than 'a'
    assert results.count("c") > results.count("a")

    # Empty choices should raise ValueError
    with pytest.raises(ValueError, match="Choices cannot be empty."):
        rng.weighted_choice({})

    # choice_enum_item: test with a simple Enum
    import enum
    class Color(enum.Enum):
        RED = 1
        GREEN = 2
        BLUE = 3

    enum_item = rng.choice_enum_item(Color)
    assert enum_item in list(Color)
