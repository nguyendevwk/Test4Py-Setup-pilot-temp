import pytest
from mimesis.random import Random
from enum import Enum


class DummyEnum(Enum):
    A = 1
    B = 2
    C = 3


def test_randints_and_uniform_consistency():
    rng = Random(42)
    # randints should return a list of the requested length with values in [a, b)
    ints = rng.randints(n=5, a=10, b=20)
    assert isinstance(ints, list)
    assert len(ints) == 5
    assert all(10 <= i < 20 for i in ints)

    # uniform should produce a float within [a, b) and respect precision
    val = rng.uniform(0.0, 1.0, precision=3)
    assert 0.0 <= val < 1.0
    # precision 3 means at most 3 decimal places
    assert round(val, 3) == val


def test_generate_string_by_mask_and_weighted_choice():
    rng = Random(123)
    # generate_string_by_mask should replace placeholders correctly
    code = rng.generate_string_by_mask(mask="@@##", char="@")
    assert len(code) == 4
    assert code[0].isupper() and code[1].isupper()
    assert code[2].isdigit() and code[3].isdigit()

    # weighted_choice should return a key according to weights
    choices = {"x": 1.0, "y": 3.0, "z": 6.0}
    result = rng.weighted_choice(choices)
    assert result in choices
    # Running multiple times should reflect weight distribution roughly
    results = [rng.weighted_choice(choices) for _ in range(1000)]
    assert results.count("z") > results.count("y") > results.count("x")


def test_error_conditions_and_choice_enum_item():
    rng = Random(0)
    # randints with non-positive n should raise ValueError
    with pytest.raises(ValueError, match="n must be greater than 0"):
        rng.randints(n=0)

    # generate_string_by_mask with same placeholder should raise ValueError
    with pytest.raises(ValueError, match="The same placeholder"):
        rng.generate_string_by_mask(mask="@@##", char="#", digit="#")

    # weighted_choice with empty dict should raise ValueError
    with pytest.raises(ValueError, match="Choices cannot be empty"):
        rng.weighted_choice({})

    # choice_enum_item should return a member of the enum
    enum_item = rng.choice_enum_item(DummyEnum)
    assert enum_item in DummyEnum
